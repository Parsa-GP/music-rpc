import sys

def main():
    if len(sys.argv) > 1:
        cmus_status = " ".join(sys.argv[1:])
        print("CMUS Status Change:", cmus_status)

if __name__ == "__main__":
    main()
