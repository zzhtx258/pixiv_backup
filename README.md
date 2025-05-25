# Pixiv Bookmark Backuper
This is a tool for backing up pixiv favorites in one click.

## Usage
First install requirements
```bash
pip install -r requirements.txt
```
Then enter the command to run the program:
```bash
python downloader.py
```
Users need to enter their user id and password upon the first time they use this tool. After that, a token text file will be created and no need to enter them the next time.

Then the tool creates two directories: "private" and "public", where the bookmarked images were downloaded to.

## License
[MIT](https://choosealicense.com/licenses/mit/)
