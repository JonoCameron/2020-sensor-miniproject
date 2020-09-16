# Task 0

The welcome message sent to the client upon initial conncetion with the server is "ECE Senior Capstone IoT simulator". Disappointingly dull.

# Task 1

I added code to client.py so that the data the client receives is placed in a file, the file name being an argument passed to the program in the command line. I wrote the JSON data to the file be using file handles, rather than changing standard out from the command line to the file. This meant that the JSON data was printed to the command line and also written to the file.

# Task 2

Using statistics and scipy.stats I calculated the median and variance of the temperature and occupancy data for class1 and plotted the Probability Density Function (PDF) of the temperature, occupancy and co2 levels of the same room. 

# Occupancy PDF
![image info](./media/occuPDF.PNG)

# Temperature PDF
![image info](./media/tempPDF.PNG)

# CO2 PDF
![image info](./media/co2PDF.PNG)

