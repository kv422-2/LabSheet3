import sqlite3 
from tabulate import tabulate #importing tabulate in order to show tabular outputs in the DBOperations print_query_result_multiple() method

# Define DBOperation class to manage all data into the database.

class DBOperations:
  # Database Name
  databaseName = "FlightDatabase.db"
  # Strings used to create and populate table if they don't exist
  pilots_table_creation = "CREATE TABLE IF NOT EXISTS Pilots (PilotNumber INTEGER NOT NULL,PilotName VARCHAR(20) NOT NULL, PRIMARY KEY (PilotNumber))"
  pilots_table_population = "INSERT OR IGNORE INTO Pilots (PilotNumber, PilotName) VALUES (1, 'John Doe'),(2, 'Jane Smith'),(3, 'Alice Johnson'),(4, 'Bob Brown'),(5, 'Charlie Davis'),(6, 'Diana Miller'),(7, 'Evan Wilson'),(8, 'Fiona Clark');"
  destinations_table_creation ="CREATE TABLE IF NOT EXISTS Destinations (AirportIdentifier VARCHAR(4) NOT NULL, AirportName VARCHAR(20) NOT NULL, AirportClosestCity VARCHAR(20) NOT NULL, PRIMARY KEY (AirportIdentifier))"
  destinations_table_population ="INSERT OR IGNORE INTO Destinations (AirportIdentifier, AirportName, AirportClosestCity) VALUES('LAX', 'Los Angeles International', 'Los Angeles'),('JFK', 'John F. Kennedy International', 'New York City'),('ORD', 'OHare International', 'Chicago'),('ATL', 'Hartsfield-Jackson Atlanta International', 'Atlanta'),('SFO', 'San Francisco International', 'San Francisco'),('DFW', 'Dallas Fort Worth International', 'Dallas'),('MIA', 'Miami International', 'Miami'),('SEA', 'Seattle-Tacoma International', 'Seattle');"
  flights_table_creation ="CREATE TABLE IF NOT EXISTS Flights (FlightNumber INTEGER NOT NULL,FlightDepartureTime DATETIMEOFFSET NOT NULL,FlightStatus VARCHAR(20) NOT NULL,PilotNumber INTEGER NOT NULL,CopilotNumber INTEGER NOT NULL,FlightOrigin VARCHAR(4) NOT NULL,FlightDestination VARCHAR(4) NOT NULL,PRIMARY KEY (FlightNumber),FOREIGN KEY (PilotNumber) REFERENCES Pilots(PilotNumber) ON DELETE RESTRICT,FOREIGN KEY (CopilotNumber) REFERENCES Pilots(PilotNumber) ON DELETE RESTRICT,FOREIGN KEY (FlightOrigin) REFERENCES Destinations(AirportIdentifier) ON DELETE RESTRICT,FOREIGN KEY (FlightDestination) REFERENCES Destinations(AirportIdentifier) ON DELETE RESTRICT)"
  flights_table_population = "INSERT OR IGNORE INTO Flights (FlightNumber, FlightDepartureTime, FlightStatus, PilotNumber, CopilotNumber, FlightOrigin, FlightDestination) VALUES(101, '2025-02-04T08:00:00-05:00', 'On Time', 1, 2, 'LAX', 'JFK'),(102, '2025-02-04T12:00:00-05:00', 'Delayed', 3, 4, 'ORD', 'ATL'),(103, '2025-02-04T14:00:00-05:00', 'On Time', 2, 3, 'JFK', 'ORD'),(104, '2025-02-04T16:00:00-05:00', 'Cancelled', 4, 1, 'ATL', 'LAX'),(105, '2025-02-04T18:00:00-05:00', 'On Time', 5, 6, 'SFO', 'DFW'),(106, '2025-02-05T08:00:00-05:00', 'Delayed', 7, 8, 'MIA', 'SEA'),(107, '2025-02-05T10:00:00-05:00', 'On Time', 1, 3, 'LAX', 'ATL'),(108, '2025-02-05T12:00:00-05:00', 'On Time', 2, 4, 'JFK', 'SFO'),(109, '2025-02-05T14:00:00-05:00', 'Cancelled', 3, 5, 'ORD', 'DFW'),(110, '2025-02-05T16:00:00-05:00', 'Delayed', 4, 6, 'ATL', 'SEA'),(111, '2025-02-05T18:00:00-05:00', 'On Time', 5, 7, 'SFO', 'MIA'),(112, '2025-02-06T08:00:00-05:00', 'On Time', 6, 8, 'DFW', 'LAX'),(113, '2025-02-06T10:00:00-05:00', 'On Time', 7, 1, 'SEA', 'JFK'),(114, '2025-02-06T12:00:00-05:00', 'Delayed', 8, 2, 'MIA', 'ORD'),(115, '2025-02-06T14:00:00-05:00', 'Cancelled', 1, 4, 'LAX', 'DFW');"

  #Strings used in methods in DBOperations
  sql_insert = "INSERT OR IGNORE INTO Flights (FlightNumber, FlightDepartureTime, FlightStatus, PilotNumber, CopilotNumber, FlightOrigin, FlightDestination) VALUES "
  sql_select_all = "SELECT * FROM Flights"
  sql_search = "SELECT * FROM Flights where FlightNumber = ?"
  sql_update_data = "UPDATE SUBSTITUTE_TABLE_NAME SET SUBSTITUTE_FIELD_NAME = ? WHERE SUBSTITUTE_IDENTIFIER_FIELD = ?"
  sql_delete_data = "DELETE FROM Flights WHERE FlightNumber = ?"
  sql_search_data_by_pilot = 'SELECT * FROM Flights WHERE PilotNumber = ?'
  sql_select_all_destinations = 'SELECT * FROM Destinations'
  sql_search_flight_data = 'SELECT * FROM SUBSTITUTE_TABLE_NAME WHERE SUBSTITUTE_FIELD_NAME = ?'

  def __init__(self):
    self.conn = sqlite3.connect(self.databaseName)
    try:
      self.cur = self.conn.cursor()
      # The Pilots and Destinations tables are populated if they don't exist, even without the user's input
      self.cur.execute(self.pilots_table_creation)
      self.cur.execute(self.pilots_table_population)
      self.cur.execute(self.destinations_table_creation)
      self.cur.execute(self.destinations_table_population)
      self.conn.commit()
    except Exception as e:
      print("EXCEPTION: "+ str(e))
    finally:
      self.conn.close()

  # get_connection establishes connection with the database 
  def get_connection(self):
    self.conn = sqlite3.connect(self.databaseName)
    self.cur = self.conn.cursor()

  # create_table populates the Flights table upon its invocation by the user's input
  def create_table(self):
    try:
      self.get_connection()
      self.cur.execute(self.flights_table_creation)
      self.cur.execute(self.flights_table_population)
      self.conn.commit()
      print("Flights Table created successfully. If it didn't exist before, it does now!")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # insert_data allows the user to insert a row into the Flights table based on their inputs
  def insert_data(self):
    try:
      self.get_connection()
       # The FlightInfoclass is used to store information about the Flight being added
      flight = FlightInfo()
      flight.set_flight_id(int(input("Enter FlightID: ")))
      flight.set_flight_origin(str(input("Enter Flight Origin: ")))
      flight.set_flightDepartureTime(str(input("Enter Flight Departure Time (Example Format: 2025-02-04T16:00:00-05:00): ")))
      flight.set_flight_destination(str(input("Enter Flight Destination: ")))
      flight.set_flight_status(str(input("Enter Flight Status: ")))
      flight.set_PilotNumber(str(input("Enter Pilot's Pilot Number: ")))
      flight.set_CopilotNumber(str(input("Enter Copilot's Pilot Number: ")))

       # The FlightInfoclass is used to add the flight to the Flights table
      self.cur.execute(self.sql_insert + str(tuple(str(flight).split("\n"))) +";")
      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # print_query_result_multiple is used by other methods in the DBOperations class in order to show tabular results
  def print_query_result_multiple(self,result,header_list):
    tabulate_table = tabulate(result,header_list,tablefmt="grid")
    print(tabulate_table)

  # select_all uses the print_query_result_multiple method to show all entries in the Flights table upon its invocation by the user's input
  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all+";")
      result = self.cur.fetchall()
      self.print_query_result_multiple(result,["FlightNumber","FlightDepartureTime","FlightStatus","PilotNumber","CopilotNumber","FlightOrigin","FlightDestination"])
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # print_query_result_single is used by other methods in the DBOperations class in order to show a single Flight's information
  def print_query_result_single(self,result):
    if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Flight ID: " + str(detail))
          elif index == 1:
            print("Flight Departure Time: " + detail)
          elif index == 2:
            print("Flight Status: " + detail)
          elif index == 3:
            print("Flight Pilot: " + str(detail))
          elif index == 4:
            print("Flight Copilot: " + str(detail))
          elif index == 5:
            print("Flight Origin: " + detail)
          elif index == 6:
            print("Flight Destination: " + detail)
          else:
            print("Extra Info: " + str(detail))
    else:
      print("No Record")

  # search_data uses the print_query_result_single method to show a single entry in the Flights table upon its invocation by the user's input
  def search_data(self):
    try:
      self.get_connection()
      flightID = int(input("Enter FlightNo: "))
      self.cur.execute(self.sql_search, tuple([str(flightID)]))
      result = self.cur.fetchone()
      self.print_query_result_single(result)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # update_data uses user inputs to update a specific value in a specific table of the user's choosing upon its invocation by the user's input
  def update_data(self):
    try:
      self.get_connection()
      # Update statement
      table_name = input("Enter table name: ")
      field_name = input("Enter field name to update: ")
      new_value = input("Enter new value: ")
      identifier_field = input("Enter the identifier field name: ")
      identifier_value = input("Enter the identifier value: ")
      self.get_connection()
      # substition via the .replace() method is used to modify the text in the string to be included in the execution
      sql_update_data_after_substitution = (self.sql_update_data.replace("SUBSTITUTE_TABLE_NAME", table_name).replace("SUBSTITUTE_FIELD_NAME", field_name).replace("SUBSTITUTE_IDENTIFIER_FIELD", identifier_field))
      self.cur.execute(sql_update_data_after_substitution, tuple([str(new_value),str(identifier_value)]))
      
      # if a row is affected, it is noted, otherwise a message is shown
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + "Row(s) affected.")
        self.conn.commit()
        print("Data Updated Successfully!")
      else:
        print("Cannot find this record in the database")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  # delete_data deletes Flight data from the table based on the user's chosen FlightNumber upon its invocation by the user's input
  def delete_data(self):
    try:
      self.get_connection()
      identifier_value = input("Enter the FlightNumber to be deleted: ")
      self.cur.execute(self.sql_delete_data, tuple([str(identifier_value)]))
      
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + "Row(s) affected.")
        self.conn.commit()
        print("Data Deleted Successfully!")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  # pilot_assignment updates the PilotNumber associated with a particular FlightNumber upon its invocation by the user's input 
  def pilot_assignment(self):
    try:
      self.get_connection()

      # Update statement
      table_name = 'Flights'
      field_name = 'PilotNumber'
      new_value = input("Enter Pilot Number for Assignment: ")
      identifier_field = 'FlightNumber'
      identifier_value = input("Enter the FlightNumber for Assignment value: ")
      self.get_connection()
      sql_update_data_after_substitution = (self.sql_update_data.replace("SUBSTITUTE_TABLE_NAME", table_name).replace("SUBSTITUTE_FIELD_NAME", field_name).replace("SUBSTITUTE_IDENTIFIER_FIELD", identifier_field))
      self.cur.execute(sql_update_data_after_substitution, tuple([str(new_value),str(identifier_value)]))
      
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + "Row(s) affected.")
        self.conn.commit()
        print("Data Updated Successfully!")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # view_pilot_schedule uses the print_query_result_multiple method to show all entries in the Flights table for a particular PilotNumber upon its invocation by the user's input
  def view_pilot_schedule_by_pilot_number(self):
    try:
      self.get_connection()
      identifier_value = input("Enter Your Pilot Number: ")
      self.cur.execute(self.sql_search_data_by_pilot,tuple([str(identifier_value)]))
      result = self.cur.fetchall()
      print("Here's your schedule: ")
      self.print_query_result_multiple(result,["FlightNumber","FlightDepartureTime","FlightStatus","PilotNumber","CopilotNumber","FlightOrigin","FlightDestination"])
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # view_destinations uses the print_query_result_multiple method to show all entries in the Destinations table upon its invocation by the user's input
  def view_destinations(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all_destinations)
      result = self.cur.fetchall()
      self.print_query_result_multiple(result,["AirportIdentifier","AirportName","AirportClosestCity"])
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # update_destinations uses user inputs to update a specific value of the user's choosing in the Destinations table upon its invocation by the user's input
  def update_destinations(self):
    try:
      self.get_connection()

      # Update statement
      table_name = 'Destinations'
      field_name = input("Enter field name to update in the Destinations table: ")
      new_value = input("Enter new value for this field: ")
      identifier_field = 'AirportIdentifier'
      identifier_value = input("Enter the AirportIdentifier you'd like to update: ")
      self.get_connection()
      sql_update_data_after_substitution = (self.sql_update_data.replace("SUBSTITUTE_TABLE_NAME", table_name).replace("SUBSTITUTE_FIELD_NAME", field_name).replace("SUBSTITUTE_IDENTIFIER_FIELD", identifier_field))
      self.cur.execute(sql_update_data_after_substitution, tuple([str(new_value),str(identifier_value)]))
      
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + "Row(s) affected.")
        self.conn.commit()
        print("Data Updated Successfully!")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # search_by_field uses the print_query_result_multiple method to show all entries in the Flights table matching the user's input upon its invocation by the user's input
  def search_by_field(self):
    try:
      table_name = 'Flights'
      field_name = input("Enter a search criteria from the Flights table: ")
      search_value = input("Enter the value you're looking for in this field: ")
      self.get_connection()
      sql_update_data_after_substitution = (self.sql_search_flight_data.replace("SUBSTITUTE_TABLE_NAME", table_name).replace("SUBSTITUTE_FIELD_NAME", field_name))
      self.cur.execute(sql_update_data_after_substitution, tuple([str(search_value)]))
      result = self.cur.fetchall()
      self.print_query_result_multiple(result,["FlightNumber","FlightDepartureTime","FlightStatus","PilotNumber","CopilotNumber","FlightOrigin","FlightDestination"])
      
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


#the FlightInfo class is used for temporarily stored Flight information before it is loaded into the database
class FlightInfo:

  def __init__(self):
    self.flightID = 0
    self.flightDepartureTime =''
    self.PilotNumber = ''
    self.CopilotNumber = ''
    self.flightOrigin = ''
    self.flightDestination = ''
    self.status = ''

  def set_flight_id(self, flightID):
    self.flightID = flightID

  def set_flightDepartureTime(self, flightDepartureTime):
    self.flightDepartureTime = flightDepartureTime

  def set_PilotNumber(self, PilotNumber):
    self.PilotNumber = PilotNumber

  def set_CopilotNumber(self, CopilotNumber):
    self.CopilotNumber = CopilotNumber

  def set_flight_origin(self, flightOrigin):
    self.flightOrigin = flightOrigin

  def set_flight_destination(self, flightDestination):
    self.flightDestination = flightDestination

  def set_flight_status(self, status):
    self.status = status

  def get_flight_id(self):
    return self.flightID

  def get_flightDepartureTime(self):
    return self.flightDepartureTime
  
  def get_PilotNumber(self):
    return self.PilotNumber
  
  def get_CopilotNumber(self):
    return self.CopilotNumber
  
  def get_flight_origin(self):
    return self.flightOrigin

  def get_flight_destination(self):
    return self.flightDestination

  def get_status(self):
    return self.status

  # the __str__ method allows one to change how FlightInfo instances are casted when casted as strings
  def __str__(self):
    return str(self.get_flight_id()) + "\n" + self.get_flightDepartureTime() + "\n" + self.get_status()  + "\n" + self.get_PilotNumber()  + "\n" + self.get_CopilotNumber() + "\n" + self.get_flight_origin() + "\n" + self.get_flight_destination()


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.

while True:
  print("\n Menu:")
  print("**********")
  print(" 1. Create table Flights")
  print(" 2. Insert data into Flights")
  print(" 3. Select all data from Flights")
  print(" 4. Search By FlightNumber")
  print(" 5. Update data some records")
  print(" 6. Delete a flight from Flights")
  print(" 7. Assign Pilot to Flight")
  print(" 8. View Pilot Schedule By Pilot Number")
  print(" 9. View Destinations")
  print(" 10. Update Destinations")
  print(" 11. Search for some Flights")
  print(" 12. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    db_ops.pilot_assignment()
  elif __choose_menu == 8:
    db_ops.view_pilot_schedule_by_pilot_number()
  elif __choose_menu == 9:
    db_ops.view_destinations()
  elif __choose_menu == 10:
    db_ops.update_destinations()
  elif __choose_menu == 11:
    db_ops.search_by_field()
  elif __choose_menu == 12:
    exit(0)
  else:
    print("Invalid Choice")
