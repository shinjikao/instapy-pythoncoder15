from instapy import InstaPy

session = InstaPy(username='**********', password='***********')
d
session.login()

session.set_relationship_bounds(
	enabled=True,
	potency_ratio=0,
	delimit_by_numbers=True,
	max_followers=60000,
    max_following=10000000000,
	min_followers=300,
	min_following=200,
	min_posts=10)

#session.set_user_interact(amount=2, percentage=100, randomize=True, media='Photo')

session.like_by_photo_likers('insert-picture-link', follow_likers_per_photo =1500 , randomize=True, sleep_delay=60, interact=False)

session.end()