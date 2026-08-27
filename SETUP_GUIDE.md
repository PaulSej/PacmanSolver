# Quick setup guide

* Clone project

```bash
git clone
```

* Create Python virtual environment

```bash
python -m venv .env
```

* Activate virtual environment
    + Windows

    ```bash
    source .env/Scripts/activate
    ```


    + Linux
    ```bash
    source .env/bin/activate
    ```


* Be sure to upgrade pip to fetch last versions of packages

```bash
python -m pip install --upgrade pip
```

* Install required dependencies from file

```bash
pip install -r requirements.txt
```

* Update browsers compatible with Playwright CLI

```bash
playwright install
```

* Some extra work is required to use the pytesseract module
    + Windows users 
        1. [Download and install the module from the installer](https://github.com/UB-Mannheim/tesseract/wiki)
        2. Add the following to your code
        ```python
            import pytesseract
            ## Replace with the path set at the previous step
            pytesseract.pytesseract.tesseract_cmd = r'C:\Users\username\AppData\Local\Programs\Tesseract-OCR\tesseract'
        ```