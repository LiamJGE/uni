using System;
using GestDep.Entities;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace GestDepLogicDesignTest
{
    [TestClass]
    public class UserTest
    {
        [TestMethod]
        public void NoParamsConstructorInitializesMaintenances()
        {
            User user = new User();
            Assert.AreNotSame(null, user, "There must be a constructor without parameters.");
            Assert.IsNotNull(user.Enrollments, "Collection of Enrollments not properly initialized. \n Patch the problem adding:  Enrollments = new List<Enrollment>();");
            Assert.AreEqual(TestData.EXPECTED_EMPTY_LIST_COUNT, user.Enrollments.Count, "Collection of Enrollments not properly initialized. \n You have added an extra element\n");
        }
        [TestMethod]
        public void ConstructorInitializesProps()
        {
            User user = new User(TestData.EXPECTED_PERSON_ADDRESS, TestData.EXPECTED_PERSON_IBAN, TestData.EXPECTED_PERSON_ID, TestData.EXPECTED_PERSON_NAME, TestData.EXPECTED_PERSON_ZIP_CODE, TestData.EXPECTED_USER_BIRTHDATE, TestData.EXPECTED_USER_RETIRED);
            Assert.AreEqual(TestData.EXPECTED_PERSON_ADDRESS, user.Address, "Address not properly initialized. Please check if you have called the constructor of the parent class by calling base(), and whether you have correctly assigned the parameters in the corresponding class.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_ID, user.Id, "Id not properly initialized.Please check if you have called the constructor of the parent class by calling base(), and whether you have correctly assigned the parameters in the corresponding class.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_IBAN, user.IBAN, "IBAN not properly initialized. Please check if you have called the constructor of the parent class by calling base(), and whether you have correctly assigned the parameters in the corresponding class.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_NAME, user.Name, "Name not properly initialized. Please check if you have called the constructor of the parent class by calling base(), and whether you have correctly assigned the parameters in the corresponding class.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_ZIP_CODE, user.ZipCode, "Zip code not properly initialized. Please check if you have called the constructor of the parent class by calling base(), and whether you have correctly assigned the parameters in the corresponding class.");
            Assert.AreEqual(TestData.EXPECTED_USER_BIRTHDATE, user.BirthDate, "Birth date not properly initialized. Check the order of the parameters and the assignment.");
            Assert.AreEqual(TestData.EXPECTED_USER_RETIRED, user.Retired, "Retired not properly initialized. Check the order of the parameters and the assignment.");

            Assert.IsNotNull(user.Enrollments, "Collection of Enrollments no properly initialized. \n Patch the problem adding:  Enrollments = new List<Enrollment>();");
            Assert.AreEqual(TestData.EXPECTED_EMPTY_LIST_COUNT, user.Enrollments.Count, "Collection of Enrollments not properly initialized. \n You have added an extra element\n");
        }
    }
}
