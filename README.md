# Schedule.py

`schedule.py` is a way of producing a different todo list everyday so that, over time, everything will get done. The files in the files directory can be named anything. You can delete the default ones or add your own.

For example, `files/kitchen` is a 30 line file, so it repeats once every 30 days, starting over on line 0 on the 1st January each year. A 10 line file will repeat once every 10 days.

## Special files

`schedule.py` doesn't require these files to run, but it handles files with the following names differently:

- `files/main` is where you would schedule events. It scans the first line of each file for a date, and it displays all the events that will happen today or tomorrow. Dates can be in `YYYY-MM-DD` format or `%j` format (Day of the year). Lines that don't begin with a number are ignored by the program so you can use them for organisation.

- `files/sticky` all lines in sticky are always displayed. I use this to keep track of what chapter is next in the books I'm reading or what row I'm on in the scarf I'm knitting.

- `files/hour` loops once an hour instead of once a day. This is where you'd put your daily routine.

## Plans

Right now, you can only edit the files with a text editor, but I'm planning to let you edit at least the `main` file from within the program itself. Unfortunately, there's a bug in the way parsedatetime handles day of the year; it always outputs the current day of the year instead of the target day of the year. Day of the year is more salient to me than day of the month so I want to use that format preferentially in `main` even though it can understand YYYY-MM-DD format too.