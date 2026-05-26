# CampusGram Project Status Report

## Overview
**Project:** CampusGram (College Instagram Clone)
**Framework:** Django (Python), HTML/CSS, Vanilla JS
**Database:** SQLite

## ✅ What is Done (Completed Features)

### 1. Backend & Database Setup
- **Django Configuration:** Project `campusgram_project` and `accounts` app successfully configured. 
- **Database Architecture:** `Profile`, `Post`, `Follow`, `Like`, and `Comment` models are fully set up.
- **Media Storage:** Configured Pillow and `MEDIA_ROOT` for image uploads (Profile pictures and Posts).
- **Signals:** Implemented Django Signals to auto-create User Profiles upon registration.

### 2. User Authentication
- **Registration (Signup):** Working signup form with email and password confirmation.
- **Login/Logout:** Custom login and logout views fully functioning.
- **Security:** `@login_required` decorators implemented to secure feed and interaction views.

### 3. Core Features
- **User Feed:** Feed page displays posts from the logged-in user and the accounts they follow.
- **Profile System:** 
  - Dynamic profile page showing user bio, avatar, follower/following counts, and a grid of posts.
  - Functional "Edit Profile" page to update Bio and Profile Image.
- **Social Interactions:**
  - **Follow/Unfollow:** Users can follow and unfollow other accounts.
  - **Liking:** Users can like and unlike posts.
  - **Commenting:** Users can leave comments on individual posts.
- **Post Creation:** Working image upload and caption form.

### 4. UI / UX Design
- **Bottom Navigation Bar:** Mobile-friendly bottom nav using Lucide icons.
- **Styling:** CSS injected into templates for the feed and profile grid to match the Instagram aesthetic.

---

## 🚧 What is Pending (To-Do & Missing Features)

### 1. Missing Core Features
- **Search / Explore Page:** 
  - *Current Status:* The Search icon (`<i data-lucide="search"></i>`) is unlinked (`#`).
  - *Required:* A search bar to find and discover other students/users on CampusGram.
- **Notifications / Activity Tab:** 
  - *Current Status:* The Heart icon (`<i data-lucide="heart"></i>`) is unlinked.
  - *Required:* A page to see who liked or commented on your posts, or who followed you.
- **Direct Messaging (Chat):** 
  - *Current Status:* No chat functionality exists. 
  - *Required:* WebSockets (Django Channels) or AJAX-based real-time messaging system.

### 2. User Interface Enhancements
- **Single Post Detail View:** Clicking a post photo on a user's profile currently does nothing (`#`). It should open the post in a modal or standalone page.
- **Follower/Following List:** Clicking the followers count on a profile should open a list showing exactly who follows the user.
- **AJAX (No Page Reloads):** 
  - Liking a post or adding a comment currently reloads the *entire* webpage. This should be handled asynchronously using Javascript `fetch()` or HTMX.

### 3. Image & Content Optimization
- **Image Cropping:** Uploaded posts are not forced into a square aspect ratio before saving. Need a JS image cropper before upload to prevent stretched images.
- **Pagination / Infinite Scroll:** The feed loads all posts at once. It needs pagination or infinite scroll for when the app gets 100+ posts.
- **Delete Functionality:** Users currently cannot delete their own posts or comments.

### 4. Code Cleanup & Refactoring
- **Unused Static Files:** `feed.html`, `script.js`, and `style.css` in the base `campusgram_project` directory are leftover mockups and should be safely deleted or moved to a static assets folder to prevent confusion.
- **File Naming:** The main run script was renamed to `app.py`. While it works, standard Django convention is `manage.py`.

---

**Summary for the Leader:**
The foundational logic (Auth, Database, CRUD operations) is solidly in place! The next immediate priority for your team should be implementing the **Search function** so users can actually find each other to follow, and converting Likes/Comments to **AJAX** so the app feels like a modern Web App rather than a traditional reloading website.
