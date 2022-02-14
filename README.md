# MPP OCR
The purpose of this API is to detect via machine learning algorithms some key elements in image/documents

## HOWTO BUILD
`docker build -t mpp-ocr .`

## HOWTO RUN
`docker run -t 5000:80 mpp-ocr:latest`

## HOWTO TEST

```
    POST on /guess_iban

    Input : 
    file : <file.pdf>

    Ouput :
        {
            "iban": "FR....12",
            "bic": "XX...XX"
        }, 
        200
```

