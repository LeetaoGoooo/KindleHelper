# KHelper

>This project should only be used for educational purposes in order to learn more about Python and PyQt5. Any commercial use is strictly prohibited.

A Kindle assistant, Kindle's best partner


## A tool to help you find books🔧

![Version](https://img.shields.io/badge/version-1.0.0-green)  ![Python Version](https://img.shields.io/badge/python-3.6+-blue) ![Support Platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)

Developed by a software developer, who just so happens to be a Kindle enthusiast, during his spare time.

KHelper is a book-finding software that (for the time being) allows you to search for books on three websites. The interface was developed using PyQt5 so it's relatively simple, yet it's simplistic interface doesn't hinder the program's effectiveness.

## 📢Disclaimer

This application is open source and free. It should only be used to learn about Python and technology in general. The search results come from the websites this program uses, and no responsibility is assumed.

## ✨Features

1. 📖Filter out annoying ads in the process of finding books
2. ❌Filter out some invalid links from the website(s)
3. ⏬Download support
4. ✈️Push support

## 💻Interface

![KHelper](http://ww1.sinaimg.cn/large/006wYWbGly1gfrkh4h2rwj30xq0pm757.jpg)

## ⚒Download/Installation

Download the respective version for your environment from [Github Releases](https://github.com/Peach-Coding/KindleHelper/releases)

## ⌨️Local Development

### Cloning

```bash
git clone https://github.com/Peach-Coding/KindleHelper.git
```

### Install the required dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python src\kindleHelper.py
```

### Unpacking

#### macOS

```bash
pip install py2app
python3 -m setup.py py2app
```

#### Windows, Linux

```bash
pip install pyinstaller
pyinstaller src\kindleHelper.spec
```

## ☑️ TODO

- [ ] Implement more websites

## 🤝 Contributions [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)

If you're interested in participating in this project, forks and PR's are welcome!

## 📜 Open source license

Based on the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.txt) open source license.
  1.  If it's made publicly accessible on the internet, it must be open source.
  2.  Can't be used for profit and no forms of advertisement are allowed.
  3.  Indicate the source of the original project.
  4.  Inherit these principles on your project.
