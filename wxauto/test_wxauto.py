"""
Quick test script for wxauto
Make sure WeChat desktop is running and you're logged in before running this script.
"""

from wxauto import WeChat

def main():
    print("Initializing WeChat instance...")
    wx = WeChat()
    
    print("Getting messages from current chat window...")
    msgs = wx.GetAllMessage()
    
    print(f"\nFound {len(msgs)} messages:")
    for msg in msgs[:5]:  # Show first 5 messages
        print(f"  - {msg.sender}: {msg.content}")
    
    # Uncomment below to send a test message to File Transfer
    # wx.SendMsg("Hello from wxauto!", who="文件传输助手")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. WeChat desktop client is running")
        print("2. You are logged into WeChat")
        print("3. All dependencies are installed")

