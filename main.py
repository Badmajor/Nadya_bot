from data.loader import bot, dp
import handlers


def main() -> None:
    dp.run_polling(bot)


if __name__ == '__main__':
    main()
