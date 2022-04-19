using System;
using GestDep.Entities;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace GestDepLogicDesignTest
{
    [TestClass]
    public class PersonTest
    {
        [TestMethod]
        public void NoParametersConstructor()
        {
            Person person = new Person();
            Assert.AreNotSame(null, person, "We need a constructor without parameters");

        }
        [TestMethod]
        public void ConstructorInitializesProps()
        {
            Person person = new Person(TestData.EXPECTED_PERSON_ADDRESS, TestData.EXPECTED_PERSON_IBAN, TestData.EXPECTED_PERSON_ID, 
                TestData.EXPECTED_PERSON_NAME, TestData.EXPECTED_PERSON_ZIP_CODE);
            Assert.AreEqual(TestData.EXPECTED_PERSON_ADDRESS, person.Address, "Address not properly initialized. Check the order of the parameters and the assignment.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_ID, person.Id, "Id not properly initialized. Check the order of the parameters and the assignment.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_IBAN, person.IBAN, "IBAN not properly initialized. Check the order of the parameters and the assignment.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_NAME, person.Name, "Name not properly initialized. Check the order of the parameters and the assignment.");
            Assert.AreEqual(TestData.EXPECTED_PERSON_ZIP_CODE, person.ZipCode, "Zip code not properly initialized. Check the order of the parameters and the assignment.");

        }
    }
}
