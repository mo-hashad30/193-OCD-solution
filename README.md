# 193 OCD Solution 

> Because refreshing the portal every 2 seconds isn't a healthy lifestyle choice... 

⚠️ **IMPORTANT DISCLAIMER** ⚠️

This project is for **EDUCATIONAL PURPOSES ONLY**. By using this script, you acknowledge and agree to the following:

1. This is an unofficial tool and is NOT affiliated with or endorsed by the Faculty of Medicine or any other institution.
2. Using automated scripts to monitor institutional portals may violate terms of service.
3. Usage of this script may result in:
   - Account suspension or termination
   - Disciplinary action from your institution
   - IP address blocking
   - Other unforeseen consequences

**USE AT YOUR OWN RISK**. The developers assume no responsibility for any consequences resulting from the use of this script.

By using this script, you take full responsibility for any outcomes and agree that you:
- Will not abuse or overload the portal servers
- Will maintain a reasonable check interval (minimum ~180 seconds)
- Accept all risks associated with automated portal access
- Will not hold the developers responsible for any consequences

---

Tired of obsessively checking the portal every 5 minutes? Can't sleep because you might miss that sweet, sweet scores? Well, congratulations! You've just found the ~~treatment of your addiction~~ solution to your problems! 

This Python script monitors the Faculty of Medicine - Cairo University portal for "Score" changes and notifies you through every possible channel (because one notification is never enough, right?), unfortunately, you can't set up alarm clock-style notifications :/.

## Features

- Automated portal stalking (professionally called "monitoring")
- Notifications:
  - Desktop notifications (in case you're actually at your computer)
  - Telegram messages (for that sweet dopamine hit on your phone)
  - Email notifications (old school, but hey, triple the anxiety!)
- Configurable check interval (minimum ~180 seconds, we're obsessed but not crazy)
- Test mode (to make sure your notification addiction is properly set up)

## Prerequisites

Before diving into this hole, you'll need:
- Python 3.x (because we're fancy)
- Chrome browser installed (probably, not 100% sure but install it anyway)
- Selenium WebDriver (included in `requirements.txt`)
- Gmail account (to spam yourself with emails)
- Telegram account

## Installation

1. Clone this masterpiece:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (where all your secrets go to hide)

## Configuration

1. Copy `.env.example` to `.env` (the hardest part of this setup, honestly):
```bash
cp .env.example .env
```

2. Fill in your credentials:

### Required Settings:
```env
PORTAL_USERNAME=your_username #20190000
PORTAL_PASSWORD=your_password #The one you use to login to the portal (duh)
```

### Optional But Highly Recommended for Maximum Notification Overdose:
Follow the Telegram and Email setup instructions in the `.env.example` file. They're like a treasure hunt, but with API tokens!

## Usage

1. Make sure everything is set up correctly in `.env`
2. Run this bad boy:
```bash
python script.py
```

3. Sit back, relax, and wait for the notifications to flood in!
   (Just kidding, we know you'll still check the portal manually)

### Test Mode
Want to make sure this actually works without waiting for actual updates?
1. Edit `script.py`
2. Set `TEST_MODE = True`
3. Run it and watch the notifications roll in!

## Contributing

Found a way to make this even more ~~obsessive~~ efficient? Pull requests are welcome! (not really, but it sounds professional to say that)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (we have no idea what that means either, but it looks legit)

---
