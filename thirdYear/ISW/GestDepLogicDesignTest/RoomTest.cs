using System;
using GestDep.Entities;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace GestDepLogicDesignTest
{
    [TestClass]
    public class RoomTest
    {
        [TestMethod]
        public void NoParamsConstructorInitializesMaintenances()
        {
            Room room = new Room();
            Assert.AreNotSame(null, room, "There must be a constructor without parameters.");
            Assert.IsNotNull(room.Activities, "Collection of Activities not properly initialized. \n Patch the problem adding:  Activities = new List<Activity>();");
            Assert.AreEqual(TestData.EXPECTED_EMPTY_LIST_COUNT, room.Activities.Count, "Collection of Activities not properly initialized. You have added an extra element\n");
        }
        [TestMethod]
        public void ConstructorInitializesProps()
        {
            Room room = new Room(TestData.EXPECTED_ROOM_NUMBER);
            Assert.AreEqual(TestData.EXPECTED_ROOM_NUMBER, room.Number, "Number not properly initialized. Check the order of the parameters and the assignment.");
            Assert.IsNotNull(room.Activities, "Collection of Activities not properly initialized. \n Patch the problem adding:  Activities = new List<Activity>();");
            Assert.AreEqual(TestData.EXPECTED_EMPTY_LIST_COUNT, room.Activities.Count, "Collection of Activities not properly initialized. You have added an extra element\n");
        }
    }
}
