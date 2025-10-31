"""
Command-line interface for build commands.
If user inputs "帮助", shows available commands.
If user inputs a command (1-5), starts processing the task.
Lock logic: only one task can run at a time. If a task is running, new commands are rejected.
Type 'exit' or 'quit' to stop the program.
"""

import threading
import time

# Task descriptions mapping
TASKS = {
    "1": "打包测试环境官网包",
    "2": "打包测试环境商店包",
    "3": "打包正式官网包",
    "4": "打包正式环境商店包",
    "5": "打包aab"
}

# Lock to track if a task is currently running
task_lock = threading.Lock()
current_task = None  # Track the current running task command number (e.g., "1")


class MockChat:
    """Mock Chat object that prints messages instead of sending them"""
    def SendMsg(self, msg):
        print(f"[REPLY] {msg}")


def process_task(task_desc, chat):
    """Process a task asynchronously (mock 10 seconds)"""
    global current_task
    
    try:
        print(f"[TASK] Started: {task_desc}")
        # Mock task processing - takes 10 seconds
        time.sleep(10)
        print(f"[TASK] Completed: {task_desc}")
    finally:
        # Release the lock when task is done
        with task_lock:
            current_task = None
            print(f"[TASK] Lock released after completing: {task_desc}")


def handle_command(input_msg, chat):
    """Handle a command input"""
    global current_task
    
    # Get the original message content
    original_msg = input_msg.strip()
    
    print(f"[INPUT] Received: {original_msg}")
    
    # Handle "帮助" command (bypasses lock)
    if original_msg == "帮助":
        help_msg = "1=打包测试环境官网包；2.打包测试环境商店包；3. 打包正式官网包；4. 打包正式环境商店包；5. 打包aab。"
        print(f"[INFO] Sending: {help_msg}")
        chat.SendMsg(help_msg)
        return
    
    # Handle exit commands
    if original_msg.lower() in ['exit', 'quit', 'q']:
        if current_task is not None:
            print(f"[WARN] Task {current_task} is still running. Please wait...")
        return "exit"
    
    # Handle command numbers (1-5)
    if original_msg in TASKS:
        print(f"[INFO] Entering TASKS block for: {original_msg}")
        
        with task_lock:
            print(f"[DEBUG] Acquired lock. current_task = {current_task}")
            # Check if a task is already running
            if current_task is not None:
                # Task is running, reject the new command
                print(f"[DEBUG] Task busy branch: current_task={current_task}")
                task_desc = TASKS[current_task]
                reply_msg = f"正在处理{current_task}={task_desc}，请稍后再来。"
                print(f"[INFO] Task busy: {current_task}. Sending: {reply_msg}")
                chat.SendMsg(reply_msg)
                return
            
            # No task running, start new task
            print(f"[INFO] Starting new task branch: {original_msg}")
            task_desc = TASKS[original_msg]
            current_task = original_msg  # Store command number (e.g., "1")
            reply_msg = f"开始处理，{original_msg}={task_desc}。"
            print(f"[INFO] Sending: {reply_msg}")
            chat.SendMsg(reply_msg)
            
            # Start task in a separate thread so it doesn't block input
            print(f"[INFO] Starting thread for task: {task_desc}")
            task_thread = threading.Thread(target=process_task, args=(task_desc, chat))
            task_thread.daemon = True
            task_thread.start()
            print(f"[DEBUG] Thread started. Thread alive: {task_thread.is_alive()}")
        
        print("[DEBUG] Exiting task_lock context")
        return
    else:
        print(f"[WARN] Command '{original_msg}' not recognized. Type '帮助' for available commands.")


def main():
    """Main command-line interface"""
    global current_task
    
    chat = MockChat()
    
    print("=" * 60)
    print("Build Command Line Interface")
    print("=" * 60)
    print("Available commands:")
    print("  帮助 - Show available commands")
    print("  1-5  - Run build tasks")
    print("  exit/quit - Exit the program")
    print("=" * 60)
    print()
    
    try:
        while True:
            try:
                # Get user input
                user_input = input("> ")
                
                if not user_input.strip():
                    continue
                
                # Handle the command
                result = handle_command(user_input, chat)
                
                # Check if user wants to exit
                if result == "exit":
                    if current_task is not None:
                        print(f"[WARN] Task {current_task} is still running.")
                        confirm = input("Are you sure you want to exit? (y/n): ")
                        if confirm.lower() != 'y':
                            continue
                    print("[INFO] Exiting...")
                    break
                    
            except KeyboardInterrupt:
                print("\n[INFO] Interrupted by user.")
                if current_task is not None:
                    print(f"[WARN] Task {current_task} is still running.")
                break
            except EOFError:
                print("\n[INFO] End of input.")
                break
                
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
