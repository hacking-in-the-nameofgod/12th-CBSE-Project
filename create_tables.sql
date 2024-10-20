create DATABASE EduTrack;
use EduTrack;

create table student (studentid varchar(8) primary key, email varchar(50) not null, studentname varchar(50) not null, passwd varchar(255) not null, classsec varchar(3) not null, school varchar(50) not null);

create table teacher (teacherid varchar(8) primary key, teachername varchar(50) not null, email varchar(50) not null, passwd varchar(255) not null, school varchar(50) not NULL);

create table class (classid varchar(8) primary key, classname varchar(50) not null);

create table studentmembership (classid varchar(8) not null, studentid varchar(8) not null);

create table teachermembership (classid varchar(8) not null, teacherid varchar(8) not null);

create table assignment (assignmentid varchar(8) primary key,classid varchar(8) not null,assignmentname varchar(50) not null,deadline date not null);

create table problem (problemid varchar(8) primary key,assignmentid varchar(8) not null,problem text not null );

create table submission (submissionid varchar(8) primary key,problemid varchar(8) not null,code text not null,complete varchar(1) not null,comments text not null);