from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Post, Notification

class CampusGramTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='rahul', password='password123')
        self.user2 = User.objects.create_user(username='priya', password='password123')
        
        # Create a test post for rahul
        self.post = Post.objects.create(
            user=self.user1,
            caption="Excited for the upcoming Hackathon! #TechFest",
            category="Event"
        )

    def test_profile_signal_creation(self):
        """Verify user registration automatically instantiates a profile."""
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)
        self.assertEqual(profile1.user.username, 'rahul')
        self.assertEqual(profile2.user.username, 'priya')

    def test_notification_creation(self):
        """Verify creating a notification stores and reads back successfully."""
        # Priya likes Rahul's post, creating a notification
        notification = Notification.objects.create(
            recipient=self.user1,
            sender=self.user2,
            post=self.post,
            notification_type='like'
        )
        
        # Retrieve notifications for Rahul
        rahul_notifs = Notification.objects.filter(recipient=self.user1)
        self.assertEqual(rahul_notifs.count(), 1)
        
        notif = rahul_notifs.first()
        self.assertEqual(notif.sender.username, 'priya')
        self.assertEqual(notif.notification_type, 'like')
        self.assertEqual(notif.post, self.post)
        self.assertFalse(notif.is_read)

