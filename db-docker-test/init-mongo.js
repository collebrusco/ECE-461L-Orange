// init-mongo.js
db = db.getSiblingDB('mydatabase');
db.createUser({
  user: 'myuser',
  pwd: 'mypassword',
  roles: ['readWrite']
});

// Insert data into the 'projects' collection
db.projects.insertOne({
  "_id": ObjectId("651a62a3b5248dbcc86fbef1"),
  "title": "Sample Project",
  "description": "Description for Sample Project",
  "resources": [
    {
      "resource_id": ObjectId("651a5a8bb5248dbcc8638dbe"),
      "quantity": 3
    },
    {
      "resource_id": ObjectId("651a5a8bb5248dbcc8638dc0"),
      "quantity": 2
    }
  ],
  "user_ids": [ObjectId("65235a9bdf748fa11b4724cd")],
  "creator_id": ObjectId("651a5a3fb5248dbcc8631798")
});


print('Database initialized successfully.');