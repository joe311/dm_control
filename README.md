# dm_control

Simple python wrapper for control of Thorlabs DMP40 deformable mirror:
https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=5056

TLDFMX_wrapper.py has most of the useful code, and provides a more 'pythonic' interface than the underlying C. 
Based on ctypes, and requires the offical drivers to be installed (in order to load a few DLLs). 
Not all features are implemented. 

Developed during the 2022 CSHL Imaging Course, in order to implement a (crude but functional) closed loop imaging optimizer.  
