// ON/OFF    sudo systemctl enable neo4j
//           sudo systemctl start neo4j 
//           sudo systemctl status neo4j
//           sudo systemctl stop neo4j

// CHECK     cypher-shell
//            - neo4j
//            - password (slide)

// BROWSER : http://localhost:7474/browser/


// CREATE DATABASE
// Example users
CREATE 
(user1:Person:User {
    uid: 'u1',
    firstName: 'John', 
    lastName: 'Doe',
    birthDate: datetime('1990-01-01T00:00:00Z'),
    username: 'johndoe',
    email: 'john.doe@example.com',
    signUp: datetime(), 
    signIn: datetime()
    }), 
(user2:Person:User {
    uid: 'u2',
    firstName: 'Jane', 
    lastName: 'Smith',
    birthDate: datetime('1995-01-01T00:00:00Z'),
    username: 'janesmith',
    email: 'jane.smite@example.com',
    signUp: datetime(),
    signIn: datetime()
    }),
(user3:Person:User {
    uid: 'u3',
    firstName: 'Alice', 
    lastName: 'Johnson',
    birthDate: datetime('1985-01-01T00:00:00Z'),
    username: 'alicejohnson',
    email: 'alice.johnson@example.com',
    signUp: datetime(),
    signIn: datetime()
    }),

// Example groups and classrooms
(group1:Group {
    uid: 'g1',
    name: 'Developers', 
    created: datetime(), 
    bio: 'A group for developers to share knowledge and collaborate on projects.'
    }),

(class1:Group:Classroom {
    uid: 'c1',
    name: 'Software Development 101', 
    created: datetime(), 
    bio: 'A classroom for beginners to learn the basics of software development.'
    }),

// Example learning modules
(lm1:Module:LearningModule {
    uid: 'lm1',
    name: 'Unit Testing 101', 
    created: datetime(), 
    modified: datetime(), 
    content: 'Unit Testing 101 is a course that teaches you how to write unit tests for your code. It covers the basics of unit testing, including what unit tests are, why they are important, and how to write them. The course also includes hands-on exercises to help you practice writing unit tests for different types of code. By the end of the course, you will have a solid understanding of unit testing and be able to write unit tests for your own code with confidence.'
    }), 
(lm2:Module:LearningModule {
    uid: 'lm2',
    name: 'Integration Testing 101', 
    created: datetime(), 
    modified: datetime(), 
    content: 'Integration Testing 101 is a course that teaches you how to write integration tests for your code. It covers the basics of integration testing, including what integration tests are, why they are important, and how to write them. The course also includes hands-on exercises to help you practice writing integration tests for different types of code. By the end of the course, you will have a solid understanding of integration testing and be able to write integration tests for your own code with confidence.'
    }),
(lm3:Module:LearningModule {
    uid: 'lm3',
    name: 'End-to-End Testing 101', 
    created: datetime(), 
    modified: datetime(), 
    content: 'End-to-End Testing 101 is a course that teaches you how to write end-to-end tests for your code. It covers the basics of end-to-end testing, including what end-to-end tests are, why they are important, and how to write them. The course also includes hands-on exercises to help you practice writing end-to-end tests for different types of code. By the end of the course, you will have a solid understanding of end-to-end testing and be able to write end-to-end tests for your own code with confidence.'
    }),

// Example relationships
(user1) -[:FRIENDS {
    created: datetime(),
    bestFriend: true
    }]-> (user2),
(user1) -[:FRIENDS {
    created: datetime(),
    bestFriend: false
    }]-> (user3),
(user1) -[:IS_IN {
    created: datetime(),
    role: 'admin'
    }]-> (group1),
(user2) -[:IS_IN {
    created: datetime(),
    role: 'user'
    }]-> (group1),
(user1) -[:IS_IN {
    created: datetime(),
    role: 'student'
    }]-> (class1),
(user2) -[:IS_IN {
    created: datetime(),
    role: 'student'
    }]-> (class1),
(user3) -[:IS_IN {
    created: datetime(),
    role: 'teacher'
    }]-> (class1),

(lm1)-[n1:NEXT]->(lm2), 
(lm2)-[n2:NEXT]->(lm3),
(user1)-[v1:VISITED {firstVisit: datetime(), lastVisit: datetime()}]->(lm1), 
(user1)-[v2:VISITED {firstVisit: datetime(), lastVisit: datetime()}]->(lm2), 
(user1)-[f:FLAGGED {created: datetime()}]->(lm2),
(class1)-[:HAS_MODULE]->(lm1),
(class1)-[:HAS_MODULE]->(lm2),
(class1)-[:HAS_MODULE]->(lm3)