import unittest
import pytest
from model.EMS import EMS
from model.User import User
from model.Event import Event
from model.Course import Course
from model.Seminar import Seminar
from model.Session import Session
from model.Guest_User import Guest_User
import database.create_table as dbCreator
import database.select_table as dbHandler
import database.insert_table as dbInserter
import database.delete_tables as dbDeleter
from datetime import datetime, timedelta
# python -m unittest test_EMS.py
class TestEms(unittest.TestCase):
    def setUp(self):
        db_name = "EMS.db"
        dbCreator.create_seminar_table(db_name)
        dbCreator.create_session_table(db_name)
        dbCreator.create_user_seminar_table(db_name)
        dbCreator.create_user_session_table(db_name)

    def tearDown(self):
        dbDeleter.delete_table('Seminar')
        dbDeleter.delete_table('Session')
        dbDeleter.delete_table('User_Seminar')
        dbDeleter.delete_table('User_Session')

    def test_successful_register_seminar(self):
        system = EMS()
        user = system.get_user('6119988')
        seminar = (1,1,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-1 22:00:00',1,100,0)
        dbInserter.insert_Seminar(seminar)
        session = (1,'Hi','Tommy','Hi',50,0,1,1)
        dbInserter.insert_Session(session)
        session = (2,'Bye','Tommy','Bye',50,0,1,1)
        dbInserter.insert_Session(session)

        test_sess = system.get_event('Session', 1)

        self.assertTrue(system.update_attendees('register', test_sess, 'Session', user.email) != 0)
        test_sess = system.get_event('Session',1)
        self.assertEqual(test_sess.noAttendees, 1)
        session1 = (1,'Hi','Tommy','Hi',50,1,1,1)
        session_list = dbHandler.select_all_products("Session")
        self.assertEqual(session_list[0], session1)

        seminar_registration = dbHandler.select_all_products("User_Seminar")
        self.assertEqual(seminar_registration[0], ('z6119988@unsw.net',1,1))
        session_registration = dbHandler.select_all_products("User_Session")
        self.assertEqual(session_registration[0], ('z6119988@unsw.net',1,1,1))

    def test_close_registrations(self):
        system = EMS()
        user = system.get_user('4119998')
        seminar = (1,0,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-1 22:00:00',1,100,0)
        dbInserter.insert_Seminar(seminar)
        session1 = (1,'Hi','Tommy','Hi',50,0,1,0)
        dbInserter.insert_Session(session1)
        session2 = (2,'Bye','Tommy','Bye',50,0,1,0)
        dbInserter.insert_Session(session2)

        test_sess = system.get_event('Session', 1)

        with pytest.raises(Exception) as e_info:
            updated = system.update_attendees('register', test_sess, 'Session', user.email)

        test_sess = system.get_event('Session',1)
        self.assertEqual(test_sess.noAttendees, 0)
        session_list = dbHandler.select_all_products("Session")
        self.assertEqual(session_list[0], session1)

    def test_cancel_registrations(self):
        system = EMS()
        user = system.get_user('4119998')
        seminar = (1,-1,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-1 22:00:00',1,100,0)
        dbInserter.insert_Seminar(seminar)
        session = (1,'Hi','Tommy','Hi',50,0,1,-1)
        dbInserter.insert_Session(session)
        session = (2,'Bye','Tommy','Bye',50,0,1,-1)
        dbInserter.insert_Session(session)

        test_sess = system.get_event('Session', 1)

        with pytest.raises(Exception) as e_info:
            updated = system.update_attendees('register', test_sess, 'Session', user.email)

        test_sess = system.get_event('Session',1)
        self.assertEqual(test_sess.noAttendees, 0)
        session1 = (1,'Hi','Tommy','Hi',50,0,1,-1)
        session_list = dbHandler.select_all_products("Session")
        self.assertEqual(session_list[0], session1)

    def test_full_register_seminar(self):
        system = EMS()
        user = system.get_user('6119988')
        seminar = (1,1,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-1 22:00:00',1,100,100)
        dbInserter.insert_Seminar(seminar)
        session1 = (1,'Hi','Tommy','Hi',50,50,1,1)
        dbInserter.insert_Session(session1)
        session2 = (2,'Bye','Tommy','Bye',50,50,1,1)
        dbInserter.insert_Session(session2)

        test_sess = system.get_event('Session', 1)

        self.assertTrue(system.update_attendees('register', test_sess, 'Session', user.email) == 0)
        test_sess = system.get_event('Session',1)
        self.assertEqual(test_sess.noAttendees, 50)
        session1 = (1,'Hi','Tommy','Hi',50,50,1,1)
        session_list = dbHandler.select_all_products("Session")
        self.assertEqual(session_list[0], session1)

        seminar_registration = dbHandler.select_products("User_Seminar", "Email", "z6119988@unsw.net")
        self.assertTrue(seminar_registration == [])
        session_registration = dbHandler.select_products("User_Session", "Email", "z6119988@unsw.net")
        self.assertTrue(session_registration == [])

    def test_active_register_seminar(self):
        system = EMS()
        user = system.get_user('6119988')
        date_format = "%Y-%m-%d %H:%M:%S"
        yesterday = str(datetime.strftime(datetime.now() - timedelta(1), date_format))
        tomorrow = str(datetime.strftime(datetime.now() + timedelta(1), date_format))
        seminar = (1,1,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00','UNSW',yesterday,tomorrow,'2018-12-1 22:00:00',1,100,0)
        dbInserter.insert_Seminar(seminar)
        session = (1,'Hi','Tommy','Hi',50,0,1,1)
        dbInserter.insert_Session(session)
        session = (2,'Bye','Tommy','Bye',50,0,1,1)
        dbInserter.insert_Session(session)

        test_sess = system.get_event('Session', 1)

        with pytest.raises(Exception) as e_info:
            updated = system.update_attendees('register', test_sess, 'Session', user.email)

        seminar_registration = dbHandler.select_all_products("User_Seminar")
        self.assertEqual(seminar_registration, [])
        session_registration = dbHandler.select_all_products("User_Session")
        self.assertEqual(session_registration, [])

    def test_successful_create_seminar(self):
        system = EMS()
        user = system.get_user('4119993')

        sem = (1,1,'Test',4119993,'Testing','2018-12-10 22:00:00',\
        'UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-01 22:00:00',1,100,2)
        session1 = (1,'Hi','Hi','Hi',50,1,1,1)
        session2 = (2,'Bye','Bye','Bye',50,1,1,1)

        seminar = system.create_seminar(user, 'Test','Testing',\
        '2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00',\
        '2018-12-01 22:00:00',1)

        self.assertEqual(system.create_session(seminar, 'Hi','Hi','Hi', 50), 1)
        self.assertEqual(system.create_session(seminar, 'Bye','Bye','Bye',50), 1)
        self.assertTrue(len(seminar.sessions) == 2)
        self.assertEqual(system.add_seminar(seminar), 1)
        self.assertEqual(system.add_sessions(seminar), 1)

        seminar_list = dbHandler.select_all_products("Seminar")
        session_list = dbHandler.select_all_products("Session")
        self.assertTrue(seminar_list != [])
        self.assertTrue(session_list != [])
        self.assertEqual(seminar_list[0], sem)
        self.assertEqual(session_list[0], session1)
        self.assertEqual(session_list[1], session2)

    def test_invalid_user_creation(self):
        system = EMS()
        user = system.get_user("6119988")
        with pytest.raises(Exception) as e_info:
            seminar = system.create_seminar(user, 'Test','Testing',\
                '2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00',\
                '2018-12-1 22:00:00',1)

    def test_invalid_deregister(self):
        system = EMS()
        user = system.get_user("4119993")
        with pytest.raises(Exception) as e_info:
            #deregister
            seminar = system.create_seminar(user, 'Test','Testing',\
                '2019-01-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00',\
                '2018-12-1 22:00:00',1)

    def test_invalid_start(self):
        system = EMS()
        user = system.get_user("4119993")
        with pytest.raises(Exception) as e_info:
            seminar = system.create_seminar(user, 'Test','Testing',\
                '2018-10-10 22:00:00','UNSW','2019-02-01 22:00:00','2019-01-30 22:00:00',\
                '2018-12-1 22:00:00',1)

    def test_invalid_early(self):
        system = EMS()
        user = system.get_user("4119993")
        with pytest.raises(Exception) as e_info:
            seminar = system.create_seminar(user, 'Test','Testing',\
                 '2018-10-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00',\
                 '2018-10-11 22:00:00',1)

    def test_invalid_num_sessions(self):
        system = EMS()
        user = system.get_user('4119993')

        seminar = system.create_seminar(user, 'Test','Testing',\
        '2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00',\
        '2018-12-1 22:00:00',1)

        self.assertEqual(system.create_session(seminar, 'Hi','Hi','Hi', 50), 1)
        self.assertTrue(len(seminar.sessions) == 1)
        self.assertEqual(system.add_seminar(seminar), 0)

        seminar_list = dbHandler.select_all_products("Seminar")
        session_list = dbHandler.select_all_products("Session")
        self.assertTrue(seminar_list == [])
        self.assertTrue(session_list == [])

    def test_capacity(self):
        system = EMS()
        user = system.get_user('4119993')

        sem = (1,1,'Test',4119993,'Testing','2018-12-10 22:00:00',\
        'UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-1 22:00:00',1,100,0)
        session1 = (1,'Hi','Hi','Hi',50,0,1,1)
        session2 = (2,'Bye','Bye','Bye',50,0,1,1)

        seminar = system.create_seminar(user, 'Test','Testing',\
        '2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00',\
        '2018-12-1 22:00:00',1)

        with pytest.raises(Exception) as e_info:
            session = system.create_session(seminar, 'Hi','Hi','Hi', 0)
        with pytest.raises(Exception) as e_info:
            session = system.create_session(seminar, 'Bye','Bye','Bye',-1)

        self.assertTrue(len(seminar.sessions) == 0)

    def test_automatic_close(self):
        system = EMS()
        user = system.get_user('6119988')
        seminar = (1,1,'Test Seminar',4119993,'Testing','2018-05-25 22:00:00','UNSW','2018-05-26 10:00:00','2018-05-26 22:00:00','2018-05-25 21:00:00',1,100,2)
        dbInserter.insert_Seminar(seminar)
        session = (1,'Hi','Tommy','Hi',50,1,1,1)
        dbInserter.insert_Session(session)
        session = (2,'Bye','Tommy','Bye',50,1,1,1)
        dbInserter.insert_Session(session)

        events_left = system.open_events_list("Seminar")

        self.assertTrue(events_left == [])

    def test_duplicate_seminar(self):
        system = EMS()
        user = system.get_user('4119993')
        seminar = (1,1,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-1 22:00:00',1,100,2)
        dbInserter.insert_Seminar(seminar)
        session = (1,'Hi','Tommy','Hi',50,1,1,1)
        dbInserter.insert_Session(session)
        session = (2,'Bye','Tommy','Bye',50,1,1,1)
        dbInserter.insert_Session(session)

        seminar = system.create_seminar(user, 'Test','tested',\
        '2018-12-10 22:00:00','UNSW Law Library','2019-01-01 22:00:00','2019-01-30 22:00:00',\
        '2018-12-1 22:00:00',1)

        self.assertTrue(seminar, 0)

        seminar_list = dbHandler.select_all_products("Seminar")
        session_list = dbHandler.select_all_products("Session")
        self.assertTrue(len(seminar_list) == 1)
        self.assertTrue(len(session_list) == 2)

    def test_duplicate_seminar_different_convenor(self):
        system = EMS()
        user = system.get_user('4119998')
        seminar = (1,1,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00',\
        'UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-01 22:00:00',1,100,2)
        dbInserter.insert_Seminar(seminar)
        session = (1,'Hi','Tommy','Hi',50,0,1,1)
        dbInserter.insert_Session(session)
        session = (2,'Bye','Tommy','Bye',50,0,1,1)
        dbInserter.insert_Session(session)

        seminar = system.create_seminar(user, 'Test','tested',\
        '2018-12-10 22:00:00','UNSW Law Library','2019-01-01 22:00:00','2019-01-30 22:00:00',\
        '2018-12-1 22:00:00',1)

        self.assertTrue(seminar, 1)

        self.assertEqual(system.create_session(seminar, 'Hi','Hi','Tommy',50), 1)
        self.assertEqual(system.create_session(seminar, 'Bye','Bye','Tommy',50), 1)
        self.assertTrue(len(seminar.sessions) == 2)
        self.assertEqual(system.add_seminar(seminar), 1)
        self.assertEqual(system.add_sessions(seminar), 1)

        seminar_list = dbHandler.select_all_products("Seminar")
        session_list = dbHandler.select_all_products("Session")
        self.assertTrue(len(seminar_list) == 2)
        self.assertTrue(len(session_list) == 4)
        sem1 = (2,1,'Test',4119998,'tested','2018-12-10 22:00:00','UNSW Law Library',\
        '2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-01 22:00:00',1,100,2)
        self.assertEqual(seminar_list[1], sem1)
        session3 = (3,'Hi','Tommy','Hi',50,0,2,1)
        session4 = (4,'Bye','Tommy','Bye',50,0,2,1)
        self.assertEqual(session_list[2], session3)
        self.assertEqual(session_list[3], session4)

    def test_duplicate_session(self):
        system = EMS()
        user = system.get_user('4119993')

        seminar = system.create_seminar(user, 'Test','Testing',\
        '2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00',\
        '2018-12-1 22:00:00',1)

        self.assertEqual(system.create_session(seminar, 'Hi','Hi','Hi', 50), 1)

        self.assertEqual(system.create_session(seminar, 'Hi','Bye','Hi',50), 0)
        self.assertTrue(len(seminar.sessions) == 1)

if __name__ == '__main__':
    unittest.main()
