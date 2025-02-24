import argparse

from gui.setup_view import Setup, fix_seed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-seed", "-s", type=int, help="random video seed")
    args = parser.parse_args()
    if args.video_seed:
        fix_seed(args.video_seed)

    app = Setup()
    app.title(string="画像認識")

    app.mainloop()
