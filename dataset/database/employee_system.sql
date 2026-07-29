--
-- Database: `employee_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `hr_users`
--

CREATE TABLE `hr_users` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `mobile` varchar(15) default NULL,
  `email` varchar(100) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(100) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `hr_users`
--

INSERT INTO `hr_users` (`id`, `name`, `mobile`, `email`, `username`, `password`) VALUES
(1, 'Raj', '8929090909', 'raj@gmail.com', 'raj', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `predictions`
--

CREATE TABLE `predictions` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(50) default NULL,
  `input_data` text,
  `prediction` int(11) default NULL,
  `probability` float default NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `predictions`
--

INSERT INTO `predictions` (`id`, `username`, `input_data`, `prediction`, `probability`, `created_at`) VALUES
(1, 'raj', '{''Age'': ''35'', ''Gender'': ''Male'', ''Department'': ''Sales'', ''Job_Role'': ''Developer'', ''Education_Level'': ''Bachelor'', ''Marital_Status'': ''Single'', ''Total_Work_Experience'': ''3.4'', ''Years_At_Company'': ''2'', ''Years_In_Current_Role'': ''1'', ''Monthly_Salary'': ''20000'', ''Salary_Hike_Percent'': ''10'', ''Job_Level'': ''Level 1'', ''Overtime'': ''Yes'', ''Work_Life_Balance'': ''1'', ''Job_Satisfaction'': ''1'', ''Environment_Satisfaction'': ''0.2'', ''Relationship_With_Manager'': ''5'', ''Training_Hours_Last_Year'': ''18'', ''Performance_Rating'': ''5'', ''Distance_From_Home'': ''120'', ''Promotion_Last_5_Years'': ''Yes'', ''Absenteeism_Rate'': ''1.2'', ''Company_Stock_Option'': ''Yes''}', 1, 0.581656, '2026-04-01 23:03:57'),
(2, 'raj', '{''Age'': ''35'', ''Gender'': ''Male'', ''Department'': ''Developement'', ''Job_Role'': ''Developer'', ''Education_Level'': ''Bachelor'', ''Marital_Status'': ''Married'', ''Total_Work_Experience'': ''5'', ''Years_At_Company'': ''2'', ''Years_In_Current_Role'': ''1'', ''Monthly_Salary'': ''20000'', ''Salary_Hike_Percent'': ''10'', ''Job_Level'': ''Level 1'', ''Overtime'': ''Yes'', ''Work_Life_Balance'': ''1'', ''Job_Satisfaction'': ''1'', ''Environment_Satisfaction'': ''1'', ''Relationship_With_Manager'': ''5'', ''Training_Hours_Last_Year'': ''18'', ''Performance_Rating'': ''5'', ''Distance_From_Home'': ''10'', ''Promotion_Last_5_Years'': ''Yes'', ''Absenteeism_Rate'': ''1.2'', ''Company_Stock_Option'': ''Yes''}', 0, 0.206002, '2026-04-02 08:50:56'),
(3, 'raj', '{''Age'': ''35'', ''Gender'': ''Male'', ''Department'': ''Developement'', ''Job_Role'': ''Developer'', ''Education_Level'': ''Bachelor'', ''Marital_Status'': ''Married'', ''Total_Work_Experience'': ''5'', ''Years_At_Company'': ''2'', ''Years_In_Current_Role'': ''1'', ''Monthly_Salary'': ''20000'', ''Salary_Hike_Percent'': ''10'', ''Job_Level'': ''Level 1'', ''Overtime'': ''Yes'', ''Work_Life_Balance'': ''1'', ''Job_Satisfaction'': ''1'', ''Environment_Satisfaction'': ''1'', ''Relationship_With_Manager'': ''5'', ''Training_Hours_Last_Year'': ''18'', ''Performance_Rating'': ''5'', ''Distance_From_Home'': ''10'', ''Promotion_Last_5_Years'': ''Yes'', ''Absenteeism_Rate'': ''1.2'', ''Company_Stock_Option'': ''Yes''}', 0, 0.206002, '2026-04-02 08:51:42'),
(4, 'raj', '{''Age'': ''35'', ''Gender'': ''Male'', ''Department'': ''Developement'', ''Job_Role'': ''Developer'', ''Education_Level'': ''Bachelor'', ''Marital_Status'': ''Married'', ''Total_Work_Experience'': ''5'', ''Years_At_Company'': ''2'', ''Years_In_Current_Role'': ''1'', ''Monthly_Salary'': ''20000'', ''Salary_Hike_Percent'': ''10'', ''Job_Level'': ''Level 1'', ''Overtime'': ''Yes'', ''Work_Life_Balance'': ''1'', ''Job_Satisfaction'': ''1'', ''Environment_Satisfaction'': ''1'', ''Relationship_With_Manager'': ''5'', ''Training_Hours_Last_Year'': ''18'', ''Performance_Rating'': ''5'', ''Distance_From_Home'': ''10'', ''Promotion_Last_5_Years'': ''Yes'', ''Absenteeism_Rate'': ''1.2'', ''Company_Stock_Option'': ''Yes''}', 0, 0.206002, '2026-04-02 08:52:51'),
(5, 'raj', '{''Age'': ''35'', ''Gender'': ''Male'', ''Department'': ''Developement'', ''Job_Role'': ''Developer'', ''Education_Level'': ''Bachelor'', ''Marital_Status'': ''Married'', ''Total_Work_Experience'': ''5'', ''Years_At_Company'': ''2'', ''Years_In_Current_Role'': ''1'', ''Monthly_Salary'': ''20000'', ''Salary_Hike_Percent'': ''10'', ''Job_Level'': ''Level 1'', ''Overtime'': ''Yes'', ''Work_Life_Balance'': ''1'', ''Job_Satisfaction'': ''1'', ''Environment_Satisfaction'': ''1'', ''Relationship_With_Manager'': ''5'', ''Training_Hours_Last_Year'': ''18'', ''Performance_Rating'': ''5'', ''Distance_From_Home'': ''10'', ''Promotion_Last_5_Years'': ''Yes'', ''Absenteeism_Rate'': ''1.2'', ''Company_Stock_Option'': ''Yes''}', 0, 0.206002, '2026-04-02 08:59:12'),
(6, 'raj', '{''Age'': ''35'', ''Gender'': ''Male'', ''Department'': ''Developement'', ''Job_Role'': ''Developer'', ''Education_Level'': ''Bachelor'', ''Marital_Status'': ''Married'', ''Total_Work_Experience'': ''3.4'', ''Years_At_Company'': ''2'', ''Years_In_Current_Role'': ''1'', ''Monthly_Salary'': ''20000'', ''Salary_Hike_Percent'': ''2'', ''Job_Level'': ''Level 1'', ''Overtime'': ''Yes'', ''Work_Life_Balance'': ''1'', ''Job_Satisfaction'': ''0.1'', ''Environment_Satisfaction'': ''0'', ''Relationship_With_Manager'': ''1'', ''Training_Hours_Last_Year'': ''18'', ''Performance_Rating'': ''1'', ''Distance_From_Home'': ''120'', ''Promotion_Last_5_Years'': ''Yes'', ''Absenteeism_Rate'': ''2'', ''Company_Stock_Option'': ''No''}', 1, 0.785749, '2026-04-02 09:04:28');
