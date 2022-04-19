using System;
using GestDep.Entities;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace GestDepLogicDesignTest
{
    [TestClass]
    public class PaymentTest
    {
        [TestMethod]
        public void NoParametersConstructor()
        {
            Payment payment = new Payment();
            Assert.AreNotSame(null, payment, "There must be a constructor without parameters");
        }
        [TestMethod]
        public void ConstructorInitializesProps()
        {
            Payment payment = new Payment(TestData.EXPECTED_PAYMENT_DATE, TestData.EXPECTED_PAYMENT_DESCRIPCION, TestData.EXPECTED_PAYMENT_QUANTITY);
            Assert.AreEqual(TestData.EXPECTED_PAYMENT_DATE, payment.Date, "Date was not intialized properly. Check the order of the parameters and the assignment.");
            Assert.AreEqual(TestData.EXPECTED_PAYMENT_DESCRIPCION, payment.Description, "Description was not intialized properly. Check the order of the parameters and the assignment.");
            Assert.AreEqual(TestData.EXPECTED_PAYMENT_QUANTITY, payment.Quantity, "Quantity was not intialized properly. Check the order of the parameters and the assignment.");
        }
    }
}
