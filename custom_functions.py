
    def like_by_users_likers(
        self,
        usernames,
        photos_grab_amount=3,
        follow_likers_per_photo=3,
        photos_to_like=5,
        randomize=True,
        sleep_delay=600,
        interact=False,
        maximum_likes_per_hour=300,
        break_seconds=5
        ):
        # inspired from follow_likers()
        """ Likes users' photos likers """

        self.logger.info('Starting to like users likers...')

        if not isinstance(usernames, list):
            usernames = [usernames]

        if photos_grab_amount > 12:
            self.logger.info('Sorry, you can only grab likers from first 12 photos for given username now.\n')
            photos_grab_amount = 12

        liked_all = 0
        liked_new = 0
        relax_point = random.randint(7, 14)  # you can use some plain value `10` instead of this quitely randomized score

        for username in usernames:
            photo_urls = get_photo_urls_from_profile(self.browser,
                    username, photos_grab_amount, randomize)
            sleep(1)
            if not isinstance(photo_urls, list):
                photo_urls = [photo_urls]

            for photo_url in photo_urls:
                likers = users_liked(self.browser, photo_url,
                        follow_likers_per_photo)

                # This way of iterating will prevent sleep interference between functions

                random.shuffle(likers)
                self.like_by_users_custom(likers, photos_to_like, True, 'Photo', maximum_likes_per_hour, break_seconds)

                """
                for liker in likers[:follow_likers_per_photo]:
                    #followed = 0
                    #liked = self.like_by_users([liker], 5, True, 'Photo')
                    self.like_by_users([liker], 5, True, 'Photo')

                    self.logger.info('Liking --- ' + liker)

                    #if liked >= 0:
                    liked_all += 1
                    liked_new += 1
                    self.logger.info('Total Likes: {}'.format(str(liked_all)))
                    
                    # Custom pause
                    sleep(10)
                    self.logger.info('Taking a 10 second break\n')

                    # Take a break after a good following
                    if liked_new >= relax_point:
                        delay_random = \
                            random.randint(ceil(sleep_delay
                                * 0.85), ceil(sleep_delay * 1.14))
                        self.logger.info('------=>  Liked {} new users ~sleeping about {}'.format(liked_new,
                                ('{} seconds'.format(delay_random) if delay_random
                                < 60 else '{} minutes'.format(float('{0:.2f}'.format(delay_random
                                / 60))))))

                        #sleep(delay_random)

                        relax_point = random.randint(7, 14)
                        liked_new = 0
                        pass
                    """

        self.logger.info('Finished liking user likers!\n')
        self.logger.info('Liked users: {}'.format(liked_all))

        return self

    def like_by_photo_likers(
        self,
        photo_url,
        follow_likers_per_photo=3,
        randomize=True,
        sleep_delay=600,
        interact=False,
        ):
        """ Likes users' photos likers """

        self.logger.info('Starting to like photo likers...')

        followed_all = 0
        followed_new = 0
        relax_point = random.randint(7, 14)  # you can use some plain value `10` instead of this quitely randomized score

        likers = users_liked(self.browser, photo_url, follow_likers_per_photo)

        # This way of iterating will prevent sleep interference between functions
        random.shuffle(likers)

        self.like_by_users(likers, 2, True, 'Photo')

        self.logger.info('Finished liking photo likers!\n')

        return self

    def like_by_users_custom(self, usernames, amount=10, randomize=False, media=None, maximum_likes_per_hour=10, break_seconds=5):
        """Likes some amounts of images for each usernames"""
        if self.aborting:
            return self

        if not isinstance(usernames, list):
            usernames = [usernames]

        liked_img = 0
        total_liked_img = 0
        already_liked = 0
        inap_img = 0
        commented = 0
        followed = 0
        not_valid_users = 0
        
        # Time measurement relevant variable
        start_time = datetime.datetime.now()

        usernames = usernames or []
        self.quotient_breach = False

        for index, username in enumerate(usernames):
            if self.quotient_breach:
                break

            self.logger.info("Username [{}/{}]"
                             .format(index + 1, len(usernames)))
            self.logger.info("--> {}"
                             .format(username.encode('utf-8')))

            following = random.randint(0, 100) <= self.follow_percentage

            validation, details = self.validate_user_call(username)
            if not validation:
                self.logger.info("--> Not a valid user: {}".format(details))
                not_valid_users += 1
                continue

            try:
                links = get_links_for_username(
                    self.browser,
                    self.username,
                    username,
                    amount,
                    self.logger,
                    self.logfolder,
                    randomize,
                    media)

            except NoSuchElementException:
                self.logger.error('Element not found, skipping this username')
                continue

            if (self.do_follow and
                    username not in self.dont_include and
                    following and
                    not follow_restriction("read",
                                           username,
                                           self.follow_times,
                                           self.logger)):
                follow_state, msg = follow_user(self.browser,
                                                "profile",
                                                self.username,
                                                username,
                                                None,
                                                self.blacklist,
                                                self.logger,
                                                self.logfolder)
                if follow_state is True:
                    followed += 1
            else:
                self.logger.info('--> Not following')
                sleep(1)

            if links is False:
                continue

            # Reset like counter for every username
            liked_img = 0

            for i, link in enumerate(links):
                # Check if target has reached
                if liked_img >= amount:
                    self.logger.info('-------------')
                    self.logger.info("--> Total liked image reached it's "
                                     "amount given: {}".format(liked_img))
                    break

                if self.jumps["consequent"]["likes"] >= self.jumps["limit"][
                    "likes"]:
                    self.logger.warning(
                        "--> Like quotient reached its peak!\t~leaving "
                        "Like-By-Users activity\n")
                    self.quotient_breach = True
                    # reset jump counter after a breach report
                    self.jumps["consequent"]["likes"] = 0
                    break

                self.logger.info('Post [{}/{}]'.format(liked_img + 1, amount))
                self.logger.info(link)

                if liked_img+1==amount :
                    self.logger.info('Reached [{}/{}] - Taking a {} second break\n'.format(liked_img + 1, amount, break_seconds))
                    sleep(break_seconds)

                # Prevent too many likes per hour
                self.check_liking_speed(start_time, maximum_likes_per_hour, total_liked_img)

                try:
                    inappropriate, user_name, is_video, reason, scope = (
                        check_link(self.browser,
                                   link,
                                   self.dont_like,
                                   self.mandatory_words,
                                   self.mandatory_language,
                                   self.is_mandatory_character,
                                   self.mandatory_character,
                                   self.check_character_set,
                                   self.ignore_if_contains,
                                   self.logger))

                    if not inappropriate and self.delimit_liking:
                        self.liking_approved = verify_liking(self.browser,
                                                             self.max_likes,
                                                             self.min_likes,
                                                             self.logger)

                    if not inappropriate and self.liking_approved:
                        like_state, msg = like_image(self.browser,
                                                     user_name,
                                                     self.blacklist,
                                                     self.logger,
                                                     self.logfolder)
                        if like_state is True:
                            total_liked_img += 1
                            liked_img += 1
                            # reset jump counter after a successful like
                            self.jumps["consequent"]["likes"] = 0

                            checked_img = True
                            temp_comments = []

                            commenting = random.randint(
                                0, 100) <= self.comment_percentage

                            if self.use_clarifai and (following or commenting):
                                try:
                                    checked_img, temp_comments, \
                                    clarifai_tags = (
                                        self.query_clarifai())

                                except Exception as err:
                                    self.logger.error(
                                        'Image check error: {}'.format(err))

                            if (self.do_comment and
                                    user_name not in self.dont_include and
                                    checked_img and
                                    commenting):

                                if self.delimit_commenting:
                                    (self.commenting_approved,
                                     disapproval_reason) = verify_commenting(
                                        self.browser,
                                        self.max_comments,
                                        self.min_comments,
                                        self.comments_mandatory_words,
                                        self.logger)
                                if self.commenting_approved:
                                    # smart commenting
                                    comments = self.fetch_smart_comments(
                                        is_video,
                                        temp_comments)
                                    if comments:
                                        comment_state, msg = comment_image(
                                            self.browser,
                                            user_name,
                                            comments,
                                            self.blacklist,
                                            self.logger,
                                            self.logfolder)
                                        if comment_state is True:
                                            commented += 1

                                else:
                                    self.logger.info(disapproval_reason)

                            else:
                                self.logger.info('--> Not commented')
                                sleep(1)

                        elif msg == "already liked":
                            already_liked += 1

                        elif msg == "jumped":
                            # will break the loop after certain consecutive
                            # jumps
                            self.jumps["consequent"]["likes"] += 1

                    else:
                        self.logger.info(
                            '--> Image not liked: {}'.format(
                                reason.encode('utf-8')))
                        inap_img += 1

                except NoSuchElementException as err:
                    self.logger.error('Invalid Page: {}'.format(err))

            if liked_img < amount:
                self.logger.info('-------------')
                self.logger.info("--> Given amount not fullfilled, "
                                 "image pool reached its end\n")

        self.logger.info('User: {}'.format(username.encode('utf-8')))
        self.logger.info('Liked: {}'.format(total_liked_img))
        self.logger.info('Already Liked: {}'.format(already_liked))
        self.logger.info('Commented: {}'.format(commented))
        self.logger.info('Inappropriate: {}'.format(inap_img))
        self.logger.info('Not valid users: {}\n'.format(not_valid_users))

        self.liked_img += liked_img
        self.already_liked += already_liked
        self.commented += commented
        self.inap_img += inap_img
        self.not_valid_users += not_valid_users

        return self

    def check_liking_speed(
        self,
        start_time,
        maximum_likes_per_hour=200,
        total_liked_img=0
        ):
        """ Likes users' photos likers """

        self.logger.info('Checking liking speed...')

        now = datetime.datetime.now()
        elapsed_time = datetime.datetime.now() - start_time

        # Calculating hours - * 1000 to avoid division by zero
        days, seconds = elapsed_time.days, elapsed_time.seconds
        hours = seconds / 3600

        # Set default likes/hours to avoid division by zero error
        if total_liked_img <= 0:
            total_liked_img = 1

        self.logger.info('Total liked iamges: {} Hours: {}\n'.format(total_liked_img, hours))
        liking_speed = total_liked_img / hours

        # Show liking speed
        self.logger.info('Liking speed is [{} likes/hour]. Maximum speed is [{} likes/hour]\n'.format(liking_speed, maximum_likes_per_hour))

        # Compare liking speed
        if liking_speed > maximum_likes_per_hour:
            self.logger.info('Liking speed is higher than limit! Taking a 5 minute break!\n')            
            sleep(300)
            self.check_liking_speed(start_time, maximum_likes_per_hour, total_liked_img)
        else:
            self.logger.info('Liking speed is lower than limit! Continuing ... \n')

        self.logger.info('Finished checking speed, resuming with liking photos!\n')

        return self