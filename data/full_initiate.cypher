// ON/OFF    sudo systemctl enable neo4j
//           sudo systemctl start neo4j 
//           sudo systemctl status neo4j
//           sudo systemctl stop neo4j

// CHECK     cypher-shell
//            - neo4j
//            - password (slide)

// BROWSER : http://localhost:7474/browser/


// CREATE DATABASE
CREATE 

// NODES
// Users
(robsyc:User:Student:Teacher:Developer {username: 'robsyc', password: '1234', email: 'robbe.claeys@gmail.com'}),
(grietVH:User:Student:Teacher:Developer {username: 'grietVH', password: '0000', email: 'info@brainstorm-studiebegeleiding.be'}),
(catherineV:User:Student:Teacher {username: 'CatherineV', password: '1111', email: 'catherine@test.com'}),
(bob:User:Student {username: 'Bob', password: '2222', email: 'bob@test.com'}),
(ali:User:Student {username: 'Ali', password: '3333', email: 'ali@test.com'}),
(jef:User:Student {username: 'Jef', password: '4444', email: 'jef@test.com'}),
(jan:User:Student {username: 'Jan', password: '5555', email: 'jan@test.com'}),
(joe:User:Student {username: 'Joe', password: '6666', email: 'joe@test.com'}),
(jil:User:Student {username: 'Jil', password: '7777', email: 'jil@test.com'}),
(sandy:User {username: 'Sandy', password: '8888', email: 'sandy@test.com'}),
(randy:User {username: 'Randy', password: '9999', email: 'randy@test.com'}),
(mandy:User {username: 'Mandy', password: '1010', email: 'mandy@test.com'}),

// Classes
(brainstorm:Class {name: 'Brainstorm exam prep'}),
(murof:Class {name: 'The Murof'}),

// Contracts & Role nodes (alt: --[ROLE_IN]-> edges)
// adding intermediary nodes 
// may improve db performance
// (co_robsyc:Contract {name: 'robsyc@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_grietVH:Contract {name: 'grietVH@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_CatherineV:Contract {name: 'CatherineV@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_Bob:Contract {name: 'Bob@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_Ali:Contract {name: 'Ali@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_Jef:Contract {name: 'Jef@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_Jan:Contract {name: 'Jan@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_Joe:Contract {name: 'Joe@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),
// (co_Jil:Contract {name: 'Jil@Brainstorm_date-made', start_date: '2021-01-01', end_date: '2021-12-31'}),

// (r_Student:Role {name: 'Student'}),
// (r_Teacher:Role {name: 'Teacher'}),
// (r_Developer:Role {name: 'Developer'}),
// (r_Admin:Role {name: 'Admin'}),

// Chatrooms
(brain_chat:Chatroom {name: 'General Brainstorm chatroom'}),
(brain_chatQ:Chatroom {name: 'Med. exam questions'}),
(murof_chat:Chatroom {name: 'Shoutbox'}),
(robgriet_chat:Chatroom {name: 'robsyc-grietVH chatroom'}),
(joejil_chat:Chatroom {name: 'joe-jil chatroom'}),
(friends_chat:Chatroom {name: 'Some friends chatroom'}),

// Messages
(hello:Message {text: 'Hello, how are you?', timestamp: '2021-01-01'}),
(goodbye:Message {text: 'Goodbye, see you later!', timestamp: '2021-01-02'}),
(howdy:Message {text: 'Howdy, what are you up to?', timestamp: '2021-01-03'}),
(seeya:Message {text: 'See ya, have a good one!', timestamp: '2021-01-04'}),
(question:Message {text: 'I have a question about ...', timestamp: '2021-01-05'}),

// Learning modules
(brain1:LearningModule {name: 'Introduction to the Brainstorm medical exam prep'}),
(brain2A:LearningModule {name: 'Chemistry for dummies'}),
(brain2B:LearningModule {name: 'Physics for dummies'}),
(brain2C:LearningModule {name: 'Biology for dummies'}),
(brain3D:LearningModule {name: 'Math for dummies'}),
(brain3:LearningModule {name: 'Bringing it all together'}),
(brain4:LearningModule {name: 'The Brainstorm medicine exam'}),
(brain5:LearningModule {name: 'Medicine exam checklist'}),

(mur1:LearningModule {name: 'Hello Murof!'}),
(mur2:LearningModule {name: 'Murof for dummies'}),

// Learning module content 
(brain1cT:Content {text: 'Welcome to the Brainstorm medical exam prep!'}),
(brain1cV:Content {text: 'VIDEO FILE?!'}),
(brain2Ac:Content {text: 'Chemistry is the study of matter and the changes it undergoes.'}),
(brain2Bc:Content {text: 'Physics is the study of matter, energy, and the interactions between them.'}),
(brain2Cc:Content {text: 'Biology is the study of life and living organisms.'}),
(brain3Dc:Content {text: 'Mathematics is the study of numbers, quantities, and shapes.'}),
(brain4c:Content:Test {text: 'THIS IS A TEST!'}),

(mur1c:Content {text: 'Welcome to the Murof!'}),
(mur2c:Content {text: 'Murof is a new way of learning.'}),

// Learning module comments
(brain1cTc1:Comment {text: 'This is great!'}),
(brain1cTc2:Comment {text: 'I love it!'}),
(brain1cVq:Comment:Question {text: 'I have a question about ...'}),
(brain1cVqa:Comment:Answer {text: 'I was meant to say ...'}),

// Language nodes
(dutch:Language {name: 'Dutch'}),
(english:Language {name: 'English'}),

// Concepts (flat ontology) & Categories (hierarchical ontology)
(con1:Concept {name: 'Cell division'}),
(con2:Concept {name: 'Chemical reactions'}),
(con3:Concept {name: 'Newton\'s laws of motion'}),
(con4:Concept {name: 'Photosynthesis'}),
(con5:Concept {name: 'Mitosis'}),
(con6:Concept {name: 'Meiosis'}),
(con7:Concept {name: 'Genetics'}),
(con8:Concept {name: 'Eduction systems'}),

(cat1:Category {name: 'Organic chemistry'}),
(cat2:Category {name: 'Chemistry'}),
(cat3:Category {name: 'Biology'}),
(cat4:Category {name: 'Physics'}),
(cat5:Category {name: 'Mathematics'}),
(cat6:Category {name: 'Computer science'}),
(cat7:Category {name: 'Science'}),

// RELATIONSHIPS
// User -[:KNOWS]-> User
(grietVH)-[:KNOWS]->(catherineV),
(robsyc)-[:KNOWS]->(grietVH),
(robsyc)-[:KNOWS]->(catherineV),
(robsyc)-[:KNOWS]->(bob),
(bob)-[:KNOWS]->(ali),
(ali)-[:KNOWS]->(jef),
(jef)-[:KNOWS]->(bob),
(jil)-[:KNOWS]->(joe),

// User -[: IS_LURKING_IN / IS_STUDYING_IN / IS_COACHING_IN / IS_TEACHING_IN / IS_DEVELOPING_IN ]-> Class
(robsyc)-[:IS_DEVELOPING_IN]->(brainstorm),
(robsyc)-[:IS_DEVELOPING_IN]->(murof),
(robsyc)-[:IS_TEACHING_IN]->(murof),
(robsyc)-[:IS_TEACHING_IN]->(brainstorm),
(grietVH)-[:IS_DEVELOPING_IN]->(brainstorm),
(grietVH)-[:IS_TEACHING_IN]->(brainstorm),
(catherineV)-[:IS_TEACHING_IN]->(brainstorm),

(bob)-[:IS_STUDYING_IN]->(brainstorm),
(ali)-[:IS_COACHING_IN]->(brainstorm),
(jef)-[:IS_STUDYING_IN]->(brainstorm),
(jan)-[:IS_STUDYING_IN]->(brainstorm),
(joe)-[:IS_STUDYING_IN]->(brainstorm),
(joe)-[:IS_COACHING_IN]->(murof),
(jil)-[:IS_STUDYING_IN]->(brainstorm),

(randy)-[:IS_LURKING_IN]->(murof),
(sandy)-[:IS_LURKING_IN]->(murof),

// User / Classroom -[:HAS_CHAT]-> Chatroom
(brainstorm)-[:HAS_CHAT]->(brain_chat),
(brainstorm)-[:HAS_CHAT]->(brain_chatQ),
(murof)-[:HAS_CHAT]->(murof_chat),
(robsyc)-[:HAS_CHAT]->(robgriet_chat),
(grietVH)-[:HAS_CHAT]->(robgriet_chat),
(joe)-[:HAS_CHAT]->(joejil_chat),
(jil)-[:HAS_CHAT]->(joejil_chat),
(bob)-[:HAS_CHAT]->(friends_chat),
(ali)-[:HAS_CHAT]->(friends_chat),
(jef)-[:HAS_CHAT]->(friends_chat),

// Chatroom -[:HAS_MESSAGE]-> Message & User -[:POSTED]-> Message
(robgriet_chat)-[:HAS_MESSAGE]->(hello),
(robgriet_chat)-[:HAS_MESSAGE]->(goodbye),
(joejil_chat)-[:HAS_MESSAGE]->(howdy),
(friends_chat)-[:HAS_MESSAGE]->(seeya),
(brain_chatQ)-[:HAS_MESSAGE]->(question),

(robsyc)-[:POSTED]->(hello),
(robsyc)-[:POSTED]->(goodbye),
(joe)-[:POSTED]->(howdy),
(ali)-[:POSTED]->(seeya),
(jil)-[:POSTED]->(question),

// Classroom -[:HAS_MODULE]-> LearningModule
(brainstorm)-[:HAS_START_MODULE]->(brain1),
(brainstorm)-[:HAS_MODULE]->(brain2A),
(brainstorm)-[:HAS_MODULE]->(brain2B),
(brainstorm)-[:HAS_MODULE]->(brain2C),
(brainstorm)-[:HAS_MODULE]->(brain3D),
(brainstorm)-[:HAS_MODULE]->(brain3),
(brainstorm)-[:HAS_GOAL_MODULE]->(brain4),
(brainstorm)-[:HAS_MODULE]->(brain5),

(murof)-[:HAS_START_MODULE]->(mur1),
(murof)-[:HAS_MODULE]->(mur2),

// LearningModule -[:HAS_CONTENT]-> Content
(brain1)-[:HAS_CONTENT]->(brain1cT),
(brain1)-[:HAS_CONTENT]->(brain1cV),
(brain2A)-[:HAS_CONTENT]->(brain2Ac),
(brain2B)-[:HAS_CONTENT]->(brain2Bc),
(brain2C)-[:HAS_CONTENT]->(brain2Cc),
(brain3D)-[:HAS_CONTENT]->(brain3Dc),
(brain4)-[:HAS_CONTENT]->(brain4c),

(mur1)-[:HAS_CONTENT]->(mur1c),
(mur2)-[:HAS_CONTENT]->(mur2c),

// Comment -[:COMMENTS_ON]-> Content / Comment
(brain1cTc1)-[:COMMENTS_ON]->(brain1cT),
(brain1cTc2)-[:COMMENTS_ON]->(brain1cT),
(brain1cVq)-[:COMMENTS_ON]->(brain1cV),
(brain1cVqa)-[:COMMENTS_ON]->(brain1cVq);

// TODO
// - (LM) --[NEXT]--> (LM)
// - (LM) --[ABOUT]-> (Concept)
// - (Concept) --[REFERENCES]-> (Concept)
// - (Concept) --[IN_CATEGORY]-> (Category)
// - (Category) --[PARENT]-> (Category)
// Think more about what the (content/comment/question/answer) nodes should contain and how they should be connected to (LearningModules) & (Languages)


CREATE CONSTRAINT unqiue_username IF NOT EXISTS
FOR (u:User) REQUIRE u.username IS UNIQUE;

CREATE CONSTRAINT unqiue_classname IF NOT EXISTS
FOR (c:Class) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT unqiue_contractname IF NOT EXISTS
FOR (co:Contract) REQUIRE co.name IS UNIQUE;