from instapy import InstaPy

session = InstaPy(username='**********', password='***********')

session.login()

session.set_relationship_bounds(
	enabled=True,
    potency_ratio=0,
	delimit_by_numbers=True,
	max_followers=60000,
	max_following=10000000000,
	min_followers=400,
	min_following=300,
	min_posts=10)

#session.set_user_interact(amount=2, percentage=100, randomize=True, media='Photo')

session.like_by_users_likers(['insert-user-profile-name'], 
	photos_grab_amount = 1, 
	follow_likers_per_photo = 100, 
	photos_to_like = 3, 
	randomize=True, 
	sleep_delay=12000, 
	interact=False, 
	maximum_likes_per_hour=120, 
	break_seconds=5)

session.end()