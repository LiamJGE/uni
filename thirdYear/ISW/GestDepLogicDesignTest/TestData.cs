using System;
using GestDep.Entities;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace GestDepLogicDesignTest
{
    public class TestData
    {
        //GENERIC
        public static int EXPECTED_EMPTY_LIST_COUNT = 0;
        public static int EXPECTED_ONE_ELEMENT_LIST_COUNT = 1;
        //PERSON
        public static string EXPECTED_PERSON_ID = "94814560G";
        public static string EXPECTED_PERSON_ADDRESS = "Camí de Vera";
        public static string EXPECTED_PERSON_NAME = "Nom de prova";
        public static string EXPECTED_PERSON_IBAN = "ES6621000418401234567891";
        public static int EXPECTED_PERSON_ZIP_CODE = 46021;

        //USER
        public static DateTime EXPECTED_USER_BIRTHDATE = new Date​Time(2000, 07, 27);
        public static bool EXPECTED_USER_RETIRED = false;

        //INSTRUCTOR
        public static string EXPECTED_SSN = "ES10292421";

        //ACTIVITY
        public static Days EXPECTED_ACTIVITY_DAYS = Days.Tue | Days.Thu;
        public static string EXPECTED_ACTIVITY_DESCRIPTION = "Spinning class";
        public static TimeSpan EXPECTED_ACTIVITY_DURATION = TimeSpan.FromMinutes(60);
        public static DateTime EXPECTED_ACTIVITY_START_DATE = DateTime.Parse("2020-10-01");
        public static DateTime EXPECTED_ACTIVITY_FINISH_DATE = DateTime.Parse("2021-01-31");
        public static DateTime EXPECTED_ACTIVITY_START_HOUR = DateTime.Parse("20:00:00");
        public static int EXPECTED_MAX_ENROLLMENTS = 15;
        public static int EXPECTED_MIN_ENROLLMENTS = 5;
        public static double EXPECTED_ACTIVITY_PRICE = 1.0;

        //CITY HALL
        public static string EXPECTED_CITY_HALL_NAME = "València";

        //GYM
        public static DateTime EXPECTED_GYM_CLOSING_HOUR = DateTime.Parse("22:00:00");
        public static int EXPECTED_GYM_DISCOUNT_LOCAL = 10;
        public static int EXPECTED_GYM_DISCOUNT_RETIRED = 10;
        public static double EXPECTED_GYM_FREE_USER_PRICE = 1.0;
        public static string EXPECTED_GYM_NAME = "UPV Gym";
        public static DateTime EXPECTED_GYM_OPENING_HOUR = DateTime.Parse("07:00:00");
        public static int EXPECTED_GYM_ZIP_CODE = 46021;

        //ROOM
        public static int EXPECTED_ROOM_NUMBER = 304;

        //ENROLLMENT
        public static DateTime EXPECTED_ENROLLMENT_DATE = DateTime.Parse("2020-10-25 00:00:00");

        //PAYMENT
        public static DateTime EXPECTED_PAYMENT_DATE = DateTime.Parse("2020-10-24 23:59:59");
        public static string EXPECTED_PAYMENT_DESCRIPCION = "Spinning class enrollment payment";
        public static double EXPECTED_PAYMENT_QUANTITY = 1.0;

        public static User DEFAULT_USER = new User(EXPECTED_PERSON_ADDRESS, EXPECTED_PERSON_IBAN, EXPECTED_PERSON_ID, EXPECTED_PERSON_NAME, EXPECTED_PERSON_ZIP_CODE, EXPECTED_USER_BIRTHDATE, EXPECTED_USER_RETIRED);
        public static Activity DEFAULT_ACTIVITY = new Activity(EXPECTED_ACTIVITY_DAYS, EXPECTED_ACTIVITY_DESCRIPTION, EXPECTED_ACTIVITY_DURATION, EXPECTED_ACTIVITY_FINISH_DATE, 
            EXPECTED_MAX_ENROLLMENTS, EXPECTED_MIN_ENROLLMENTS, EXPECTED_ACTIVITY_PRICE, EXPECTED_ACTIVITY_START_DATE, EXPECTED_ACTIVITY_START_HOUR);
        public static Payment DEFAULT_PAYMENT = new Payment(EXPECTED_PAYMENT_DATE, EXPECTED_PAYMENT_DESCRIPCION, EXPECTED_PAYMENT_QUANTITY);
    }
}
