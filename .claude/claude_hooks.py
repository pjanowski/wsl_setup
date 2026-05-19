#!/usr/bin/env python3
"""Basic push notifications for Claude Code"""
import sys, json, subprocess, os, platform, shutil, argparse

SOUND_ENABLED = False
DESKTOP_ENABLED = False
NTFY_ENABLED = False

NTFY_TOPIC = "ohwellwhatevernevermindpawel"  # Change this!

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
SOUNDS = {
    "Notification": "notification.ogg",
    "Stop": "stop.wav",
    "PermissionRequest": "approval-required.mp3",
}


def play_sound(event_type):
    if not SOUND_ENABLED:
        return
    filename = SOUNDS.get(event_type)
    if not filename:
        return
    path = os.path.join(SOUNDS_DIR, filename)
    if not os.path.exists(path):
        return
    try:
        if platform.system() == "Windows":
            ps_cmd = (
                "Add-Type -AssemblyName presentationCore; "
                f"$mp = [System.Windows.Media.MediaPlayer]::new(); "
                f"$mp.Open([uri]'{path}'); "
                "$mp.Play(); Start-Sleep -Seconds 4"
            )
            subprocess.Popen(
                ["powershell", "-WindowStyle", "Hidden", "-NonInteractive", "-Command", ps_cmd],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        else:
            for player, args in [
                ("paplay", [path]),
                ("ffplay", ["-nodisp", "-autoexit", "-loglevel", "quiet", path]),
                ("aplay", [path]),
                ("mpg123", ["-q", path]),
            ]:
                if shutil.which(player):
                    subprocess.Popen(
                        [player] + args,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    )
                    break
    except Exception:
        pass


def show_desktop_notification(title, message):
    """Show a desktop toast/popup notification, non-blocking"""
    if not DESKTOP_ENABLED:
        return
    try:
        if platform.system() == "Windows":
            def ps_escape(s):
                return s.replace("'", "''").replace("\n", " ")
            t, m = ps_escape(title), ps_escape(message)
            ps_cmd = (
                "Add-Type -AssemblyName System.Windows.Forms,System.Drawing; "
                "$n = [System.Windows.Forms.NotifyIcon]::new(); "
                "$n.Icon = [System.Drawing.SystemIcons]::Information; "
                "$n.BalloonTipIcon = 'Info'; "
                f"$n.BalloonTipTitle = '{t}'; "
                f"$n.BalloonTipText = '{m}'; "
                "$n.Visible = $true; "
                "$n.ShowBalloonTip(5000); "
                "Start-Sleep -Seconds 6; "
                "$n.Dispose()"
            )
            subprocess.Popen(
                ["powershell", "-WindowStyle", "Hidden", "-NonInteractive", "-Command", ps_cmd],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        elif platform.system() == "Linux":
            if shutil.which("notify-send"):
                subprocess.Popen(
                    ["notify-send", "--app-name=Claude Code", title, message.replace("\n", " ")],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
    except Exception:
        pass


def send_notification(title, message, project, priority="default", tags=None):
    """Send notification via ntfy"""
    if not NTFY_ENABLED:
        return
    # # Rate limit: skip if we just sent a notification for this project
    # if should_rate_limit(project):
    #     return

    # # Skip if user is actively using terminal
    # if is_terminal_focused() and not is_system_idle():
    #     return

    cmd = [
        "curl", "-s",
        "-H", f"Title: {title}",
        "-H", f"Priority: {priority}",
    ]

    if tags:
        cmd.extend(["-H", f"Tags: {tags}"])

    cmd.extend(["-d", message, f"https://ntfy.sh/{NTFY_TOPIC}"])
    subprocess.run(cmd, capture_output=True)


def format_ask_user_question(tool_input):
    """Format AskUserQuestion for rich notification"""
    questions = tool_input.get("questions", [])
    if not questions:
        return "Question from Claude"

    q = questions[0]
    header = q.get("header", "")
    question = q.get("question", "")[:120]
    options = q.get("options", [])

    parts = []
    if header:
        parts.append(f"**{header}**")
    if question:
        parts.append(question)
    if options:
        opts = " | ".join([o.get("label", "") for o in options[:4]])
        parts.append(f"→ {opts}")

    return "\n".join(parts)

def handle_pre_tool_use(data):
    """Handle PreToolUse events"""
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    cwd = os.path.basename(data.get("cwd", ""))

    if tool_name == "AskUserQuestion":
        message = format_ask_user_question(tool_input)
        send_notification(
            f"❓ {cwd}",
            message,
            cwd,
            priority="high",
            tags="question"
        )
    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        # Skip safe commands
        if any(command.startswith(safe) for safe in SAFE_COMMANDS):
            return
        # Notify for potentially dangerous commands
        send_notification(
            f"⚠️ {cwd}",
            f"Command: {command[:100]}",
            cwd,
            priority="default",
            tags="warning"
        )

def handle_permission_request(data):
    """Handle PermissionRequest events"""
    tool_name = data.get("tool_name", "unknown tool")
    tool_input = data.get("tool_input", {})
    cwd = os.path.basename(data.get("cwd", ""))

    if tool_name == "Bash":
        detail = tool_input.get("command", "")[:120]
    else:
        detail = tool_name

    play_sound("PermissionRequest")
    notification_title = f"Claude Code — {cwd}" if cwd else "Claude Code"
    show_desktop_notification(notification_title, f"Needs permission: {detail}")
    send_notification(
        notification_title,
        f"Needs permission\n{detail}",
        cwd,
        priority="high",
        tags="key"
    )


def handle_stop(data):
    """Handle Stop events (task completed)"""
    cwd = os.path.basename(data.get("cwd", ""))
    play_sound("Stop")
    notification_title = f"Claude Code — {cwd}" if cwd else "Claude Code"
    show_desktop_notification(notification_title, "Task complete")
    send_notification(
        notification_title,
        "Task complete",
        cwd,
        priority="default",
        tags="white_check_mark"
    )

def handle_notification(data):
    """Handle Notification events"""
    message = data.get("message", "")
    title = data.get("title", "")
    cwd = os.path.basename(data.get("cwd", ""))

    play_sound("Notification")
    notification_title = f"Claude Code — {cwd}" if cwd else "Claude Code"
    body = f"{title}\n{message}".strip() if title else message
    show_desktop_notification(notification_title, body)
    send_notification(
        notification_title,
        body,
        cwd,
        priority="high",
        tags="bell"
    )


def main():
    global SOUND_ENABLED, DESKTOP_ENABLED, NTFY_ENABLED
    parser = argparse.ArgumentParser()
    parser.add_argument("event_type")
    parser.add_argument("--sound", action="store_true")
    parser.add_argument("--desktop", action="store_true")
    parser.add_argument("--ntfy", action="store_true")
    args = parser.parse_args()

    SOUND_ENABLED = args.sound
    DESKTOP_ENABLED = args.desktop
    NTFY_ENABLED = args.ntfy

    event_type = args.event_type
    data = json.loads(sys.stdin.read())
    cwd = os.path.basename(data.get("cwd", ""))

    handlers = {
        "PreToolUse": handle_pre_tool_use,
        "Stop": handle_stop,
        "Notification": handle_notification,
        "PermissionRequest": handle_permission_request,
    }

    handler = handlers.get(event_type)
    if handler:
        handler(data)

if __name__ == "__main__":
    main()
