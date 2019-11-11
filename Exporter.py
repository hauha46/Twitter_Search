# -*- coding: utf-8 -*-
import sys, getopt, datetime, codecs
import csv
import matplotlib.pyplot as plt
import matplotlib.dates
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(argv):

    # Title CSV file
    fieldname = ['Content', 'Keyword', 'Time', 'Retweet', 'Link', 'Tweet ID']

    #File Name
    filename = input("Name of the file: ")
    filename = filename + ".csv"

    #Dictionary stores dates
    date_dict = {}

    # Store Keyword
    keyword = ""

    # Parameters check
    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('exporter_help_text.txt', 'r')
        f.close()
        return

    try:

        opts, args = getopt.getopt(argv, "", (
            "user name=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output=",
            "lang="))

        tweetCriteria = got.manager.TweetCriteria()

        for opt, arg in opts:
            if opt == '--username':
                tweetCriteria.username = arg

            elif opt == '--since':
                tweetCriteria.since = arg

            elif opt == '--until':
                tweetCriteria.until = arg

            elif opt == '--querysearch':
                tweetCriteria.querySearch = arg
                keyword = arg
            elif opt == '--toptweets':
                tweetCriteria.topTweets = True

            elif opt == '--maxtweets':
                tweetCriteria.maxTweets = int(arg)

            elif opt == '--near':
                tweetCriteria.near = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--output':
                outputFileName = arg

            elif opt == '--lang':
                tweetCriteria.lang = arg

        print('Searching...\n')
        # Create workbook
        workbook = []

        def receiveBuffer(tweets):

            for t in tweets:
                # Insert data into temporary dict
                temp_dict = {}
                temp_dict['Content'] = t.text
                temp_dict['Keyword'] = keyword
                temp_dict['Time'] = t.date.strftime("%m/%d/%Y")
                temp_dict['Retweet'] = t.retweets
                temp_dict['Link'] = t.permalink
                temp_dict['Tweet ID'] = t.id

                # Add data to CSV file
                workbook.append(temp_dict)

                # Insert dates into date_dict
                # temp_date = t.date.strftime("%m/%d/%Y")
                temp_date = t.date.replace(hour=0, minute=0, second=0, microsecond=0)
                try:
                    date_dict[temp_date] += 1
                except:
                    date_dict[temp_date] = 1

            # Write to CSV file
            with open(filename, 'w', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldname)
                writer.writeheader()
                writer.writerows(workbook)

        # Execute the process
        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except:
        print('Arguments parser error, try -h' + arg)
    finally:
        print('Done. Output file generated "%s".' % filename)

    # Plotting
    lists = date_dict.items()  # return a list of tuples

    x, y = zip(*lists)  # unpack a list of pairs into two tuples

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.plot(x, y, '-o', color='purple')
    ax.set(xlabel="Date", ylabel="Frequency", title="Twitter Search")

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.xaxis.set_major_formatter(DateFormatter("%m/%d"))

    plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])
#     python Exporter.py --querysearch "thebestamancanbe" --since 2015-09-10 --until 2019-09-12 --maxtweets 8000
