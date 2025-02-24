from gui.setup_view import Setup
from utils.arg_utils import parse_args
from utils.random_utils import fix_seed


if __name__ == "__main__":
    args = parse_args()
    if args.video_seed:
        fix_seed(args.video_seed)

    app = Setup()
    app.title(string="画像認識")

    app.mainloop()
