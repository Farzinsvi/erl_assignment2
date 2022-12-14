#! /usr/bin/env python
'''
Module:
	AnnounceHypotesis
ROS nodes used for simulating the robot announcement. Given an hypotesis it announces it simply printing on terminal.
Service :
	/announce_service to get the hypotesis to announce
Service Client:
        /reaching_goal client call to reach the centre of the arena
        
'''
import rospy
import random
from my_erl2.srv import Announcement, AnnouncementResponse
import actionlib
from motion_plan.msg import PlanningAction, PlanningGoal


def announce_clbk(req):
    '''
    Description of the callback:
    This function retrieves the request field of the Announcement message. Inside the custom message is present the istances of classes PERSON, PLACE, WEAPON
    corresponding to the hypothesis to announce. The robot firstly reach the centre of the arena, the announce the hypothesis finally returns to the initial location.
    Args:
      srv(Announcement): data retrieved by */announce_service* topic
    Returns:
      srv(Announcement):True
    '''
    rospy.loginfo('moving at the centr of the arena')
    #reach the centre of the arena 
    client = actionlib.SimpleActionClient('reaching_goal', PlanningAction)
    client.wait_for_server()
    goal = PlanningGoal()
    goal.target_pose.pose.position.x = 0
    goal.target_pose.pose.position.y = 0
    client.send_goal(goal)
    client.wait_for_result()
    #announce the hypothesis
    rospy.loginfo('Announce to Oracle: ')
    rospy.loginfo(req.who + ' with the ' + req.what + ' in the ' + req.where)
    #return to the starting location
    actual_loc = rospy.get_param('/actual_location')
    if actual_loc == 'wp1':
        goal.target_pose.pose.position.x = 2.6
        goal.target_pose.pose.position.y = 0
    elif actual_loc == 'wp2':
        goal.target_pose.pose.position.x = -2.6
        goal.target_pose.pose.position.y = 0
    elif actual_loc == 'wp3':
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 2.6
    else:
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 0
    client.send_goal(goal)
    client.wait_for_result()
    

    return True


def main():
    # init node
    rospy.init_node('announce_service')
    # init service
    srv = rospy.Service('announce_service', Announcement, announce_clbk)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        rate.sleep()


if __name__ == '__main__':
    main()
