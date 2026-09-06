[app]

# App name
title = JARVIS

# Package name
package.name = jarvis

# Package domain
package.domain = org.aswin

# Source directory
source.dir = .

# Python files/extensions to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3,wav,ttf

# Version
version = 1.0

# Main requirements
requirements = python3,kivy,pyjnius,requests,certifi,urllib3,idna

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 1

# Android permissions
android.permissions = INTERNET,READ_CONTACTS

# Android API settings
android.api = 35
android.minapi = 23

# Android architecture
android.archs = arm64-v8a

# Keep the app name visible
android.entrypoint = org.kivy.android.PythonActivity

# Android theme
android.presplash_color = #050A10

# Don't use an icon yet
# icon.filename = %(source.dir)s/icon.png

# Don't use a presplash image yet
# presplash.filename = %(source.dir)s/presplash.png


[buildozer]

# Log level
log_level = 2

# Warn if running as root
warn_on_root = 1


[app:android]

# Android settings
android.accept_sdk_license = True

# Backup
android.allow_backup = True

# Network access
android.permissions = INTERNET,READ_CONTACTS


[buildozer:android]

# Build in debug mode initially
