from controller import AppController
from utils.arg_utils import parse_args
from utils.random_utils import fix_seed


def main() -> None:
    args = parse_args()
    if args.video_seed:
        fix_seed(args.video_seed)

    app = AppController()
    app.run()


if __name__ == "__main__":
    main()
