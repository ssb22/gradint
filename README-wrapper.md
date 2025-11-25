# Is gradint-wrapper.exe a virus?
From https://ssb22.user.srcf.net/gradint/gradint-wrapper.html
(also [mirrored on GitLab Pages](https://ssb22.gitlab.io/gradint/gradint-wrapper.html) just in case)

The genuine gradint-wrapper.exe is **not** a virus.

The Windows version of [Gradint](README.md) defaults to starting itself automatically once per day.  This is because I’ve sometimes installed it for people who say they don’t know how to start programs (!) and/or want to be reminded about their daily vocabulary practice.

(When the simpler commercial “DuoLingo” app came on the scene later, their owl picture became famous for posting reminders some people found annoying.  I was doing it first.)

Modern Windows laptops tend to hibernate rather than shut down.  Therefore it’s no longer enough to put Gradint in the “Startup” folder—I also have to run a background process to make sure the “once per day” thing works.

## Does gradint-wrapper.exe slow the computer down?
It shouldn’t!  The background process wakes up once per hour and checks to see if the computer has hibernated overnight in the meantime.  If the computer is being slow then it must have other problems, such as:

1. Multiple anti-virus programs all scanning at once (an anti-virus program is no substitute for being careful and/or using a safer operating system, but if you must have one then consider if one is sufficient because the benefits of having more are rarely worth the cost in watching them “fight each other” over disk access),
2. Malware that is unknown to the anti-virus programs, and/or excessive amounts of “advertisement” software that was either pre-loaded by a shop or downloaded by a user who can’t tell the difference between advert-supported “free” and real free (try telling them to check for GPL, Apache or similar licenses, and/or verify the reputation of the publisher; don’t trust suggestions just because they seem to be from friends or the system),
3. Disk errors on very old hardware. 

Sometimes it’s easier to replace Windows with a good GNU/Linux installation as long as the hardware is functioning.

## Why are there 3 or 4 instances of gradint-wrapper.exe?
There should normally be only one background instance, plus another if Gradint is currently open.  When Gradint is launched from the desktop or start menu, it tries to stop the other instances and start its own, but on Vista and above this sometimes fails and multiple background processes can result.  This is harmless as old ones should detect the situation next time they wake up (the code to do this has been improved in recent versions).  It’s still occasionally possible for a user to launch two Gradint windows accidentally, but you should never see more than one automatically started.

## Is it safe to Terminate gradint-wrapper.exe?
Yes, this is safe.  But it will start again next time you reboot or run Gradint.

## Is it safe to delete gradint-wrapper.exe?
That will break your Gradint installation.  gradint-wrapper.exe is not just the background process: it is also the “wrapper” for loading the main part of Gradint on Windows (I use a 2-part loader to make the Windows version easier to update from GNU/Linux).

## How do you stop Gradint from running every day?
If you upgrade to Gradint v0.9979+ you can:

* set it at installation time (by answering No to the question “Do you want Gradint to start by itself and remind you to practise?” when first run);
* change it in the advanced settings (search for disable_once_per_day and set it to 1)

Alternatively, go to Start menu > All programs > Startup, right-click on “Run gradint once per day” and delete it.  Gradint will still start the background process when you run it manually (I set that in case it fails to find the startup folder); if you want to stop this, go to Start menu > All programs > Gradint and/or desktop > Gradint, right-click on Gradint, open in Notepad, delete `once_per_day=2` and save.

## How do you uninstall Gradint?
Go to Start menu > All programs > Gradint > uninstall, or desktop > Gradint > uninstall.  If it isn’t there, try re-downloading [the Gradint installer](https://ssb22.user.srcf.net/gradint/gradint.exe) and run it—it should replace the uninstall scripts which you can then use.

## Why is Gradint not in “Add/Remove Programs”?
To get into the “Add/Remove Programs” list, a program must be installed system-wide.  Gradint does not install itself system-wide; it installs itself in your user name’s home folder (unless you have an ancient version of Windows that doesn’t have them).  This means you can install Gradint even when you don’t have permission to install system-wide programs (such as in a computer lab), but it also means Gradint cannot use the “Add/Remove Programs” list.

## Why did some anti-virus labs flag Gradint as malicious in August 2020?
On 13th August 2020, some anti-virus labs I’d never heard of (AnyRun and VirusTotal, the latter citing Antiy-AVL, CrowdStrike Falcon, K7AntiVirus, Zillya, SecureAge APEX, Jiangmin and K7GW) incorrectly tagged the Gradint installer as a malicious trojan, and a company called Netcraft even sent a take-down notice to Cambridge University Information Services and the Student-Run Computing Facility hosting my website.

After I contacted AnyRun support asking for an appeal against the “verdict: malicious activity” they had published, they confirmed their technicians decided it was a “false positive” and made that report private to the submitter, but they were unable to relay a message to the submitter that they had done so.

I don’t know if this “detection” effort was anything to do with an incident that began the same day involving 200+ attempts from DigitalOcean-owned IP addresses to issue POST requests to gradint.exe (causing over a gigabyte of traffic), which I then blocked and reported to DigitalOcean.  Since whoever it was continued to try (making another 700+ attempts over the next 5 days), we could just be looking at two separate issues that coincidentally started at about the same time.  (My report to DigitalOcean was made after Cambridge University received the take-down notice, but before I had been told about it.)

I don’t yet know what it is about the Gradint installer that these “detectors” objected to, but I suspect it’s because the Gradint installer unpacks copies of certain free and open source software components that Gradint uses, namely, Python (with its standard libraries), eSpeak, LAME, MadPlay, PTTS and SoX.  It seems that the authors of these “detectors” regarded any attempt to unpack another executable as suspicious, especially if it’s being done from an installer that is “unsigned” because I have not paid Microsoft’s extortionate fee to be a “recognised” publisher.  I’m glad to say that this was not the case with the “big” anti-virus programs (the ones I’d heard of), which did not flag Gradint as malicious on that day.

I have asked Netcraft for an explanation of their take-down request and have not yet received any reply.

## Why is the Gradint installer not signed?
As I said on the Gradint download page, I have not paid Microsoft to make me a “known publisher” (I consider it a bit extortionate of them to require this payment even for small hobby projects)—if you make sure to fetch the installer from my own page and via HTTPS, that should be ‘signature’ enough.  If you’re being really cautious then you are welcome to download the source code, install Python and all required dependencies yourself and run it that way; I simply packaged up an installer as a convenience to those Windows users who prefer a “one-click” setup, and I don’t see why I should have to pay Microsoft not to issue a warning—that seems wrong.

## Why did AnyRun say the Gradint installer uses Task Scheduler?
Some previous versions of Gradint used Task Scheduler for the “once per day” feature.  The installer for the current version of Gradint contains one call to the Task Scheduler, but only to delete the task that those old versions left, if present.

## Why did AnyRun report Bitcoin addresses in Gradint?
There are no Bitcoin addresses in Gradint.  AnyRun’s detector must have found a false positive.

## Why did AnyRun report Gradint using SearchProtocolHost.exe?
Again this appears to be a false positive. `SearchProtocolHost.exe` is a Microsoft component pre-installed on many versions of Windows that has frequently been known to misbehave, and it seems AnyRun’s detector misidentified it as being run by Gradint on that occasion. 
