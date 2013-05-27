CRAWLER
=======

#To Install:

pip install -r requirements.txt


#Try:

    python test_scraper.py fao lis 1-12-2013 12-12-2013


#Except:

    Because it's just a proof of concept it has a few issues:

    The dates have to be written in this format 'dd-mm-yyyy'

    The airport ids have to be written

    Has no tests

    It only takes 4 arguments but it's easy to configure to at test_scraper

    Sometimes it will freeze in the request like the connection got lost this is most probably something very easy to fix that eluded my knowledge

    When there are no results nothing happends


#Finally:

    The results will be writen in file results.txt

