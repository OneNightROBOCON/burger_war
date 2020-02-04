<?xml version="1.0" ?>
<sdf version="1.4">
<world name="onigiri_field">

<scene>
  <shadows>false</shadows>
</scene>

<physics name="ode_100iters" type="ode">
  <real_time_update_rate>1000</real_time_update_rate>
  <max_step_size>0.001</max_step_size>
</physics>

<gui>
  <camera name="camera">
    <pose>1.5 -5. 6. 0.0 .85 1.8</pose>
    <view_controller>orbit</view_controller>
  </camera>
</gui>
<include><uri>model://sun</uri></include>
<include><uri>model://my_ground_plane</uri></include>

@{box_count = 0}
@{tag_count = 1}
<!-- Centor BOX -->
<include>
  <name>box_@(box_count)</name>
  <pose>0 0 0.1 0 0 0</pose>
  <uri>model://center_box</uri>
</include>
<include>
  <name>plate_@(tag_count)</name>
  <pose>0 0.1755 0.1 0 0 0</pose>
  <uri>model://plate</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>0 0.176 0.1 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.03 0.001 0.03</size></box></geometry>
      <material>
        <script>
          <uri>model://tags</uri> <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<include>
  <name>plate_@(tag_count)</name>
  <pose>0 -0.1755 0.1 0 0 0</pose>
  <uri>model://plate</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>0 -0.176 0.1 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.03 0.001 0.03</size></box></geometry>
      <material>
        <script>
          <uri>model://tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<include>
  <name>plate_@(tag_count)</name>
  <pose>0.1755 0 0.1 0 0 1.571</pose>
  <uri>model://plate</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>0.176 0 0.1 0 0 1.571</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.03 0.001 0.03</size></box></geometry>
      <material>
        <script>
          <uri>model://tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<include>
  <name>plate_@(tag_count)</name>
  <pose>-0.1755 0 0.1 0 0 1.571</pose>
  <uri>model://plate</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>-0.176 0 0.1 0 0 1.571</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.03 0.001 0.03</size></box></geometry>
      <material>
        <script>
          <uri>model://tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
@{box_count += 1}

<!-- Corner BOX -->
@{side_pos = 0.53}
@[for x in [side_pos, -side_pos]]
@[for y in [side_pos, -side_pos]]
<include>
  <name>box_@(box_count)</name>
  <pose>@(x) @(y) 0.1 0 0 0</pose>
  <uri>model://corner_box</uri>
</include>
<include>
  <name>plate_@(tag_count)</name>
  <pose>@(x) @(y+0.08) 0.1 0 0 0</pose>
  <uri>model://plate</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>@(x) @(y+0.085) 0.1 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.03 0.001 0.03</size></box></geometry>
      <material>
        <script>
          <uri>model://tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<include>
  <name>plate_@(tag_count)</name>
  <pose>@(x) @(y-0.08) 0.1 0 0 0</pose>
  <uri>model://plate</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>@(x) @(y-0.085) 0.1 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.03 0.001 0.03</size></box></geometry>
      <material>
        <script>
          <uri>model://tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
@{box_count += 1}
@[end for]
@[end for]

<!-- WALL -->
@{import math}
@[def wall(p1, p2, height)]
  @{wall.count += 1}
  @{thickness_x = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)}
  @{thickness_y = 0.0001}
  @{pose_x = (p1[0]+p2[0])/2.}
  @{pose_y = (p1[1]+p2[1])/2.}
  @{pose_z = height/2.}
  @{pose_th =  math.atan2(p2[1]-p1[1],p2[0]-p1[0])}

  <model name="wall_@(wall.count)">
    <static>true</static>
    <pose>@(pose_x) @(pose_y) @(pose_z) 0 0 @(pose_th)</pose>
    <link name="link">
      <collision name='visual'>
        <geometry>
          <box>
            <size>@(thickness_x) @(thickness_y) @(height)</size>
          </box>
        </geometry>
      </collision>
      <visual name='visual'>
        <geometry>
          <box>
            <size>@(thickness_x) @(thickness_y) @(height)</size>
          </box>
        </geometry>
        <material>
          <script>
            <uri>model://wall</uri>
            <name>wall_@(wall.count)</name>
          </script>
        </material>
      </visual>
    </link>
  </model>
@[end def]
@{wall.count = 0}
@{wall_size = 1.697}
@( wall((0, wall_size), (wall_size, 0), 0.3) )
@( wall((wall_size, 0), (0, -wall_size), 0.3) )
@( wall((0, -wall_size), (-wall_size, 0), 0.3) )
@( wall((-wall_size, 0), ( 0, wall_size), 0.3) )

<!-- RED and BLUE maker -->
<model name="blue_maker">
  <static>true</static>
  <link name="link">
    <visual name="visual">
      <pose>0 3 0 0 0 0</pose>
      <geometry>
        <cylinder>
          <radius>0.3</radius>
          <length>0.1</length>
        </cylinder>
      </geometry>
      <material><script><name>Gazebo/Blue</name></script></material>
    </visual>
  </link>
</model>
<model name="red_maker">
  <static>true</static>
  <link name="link">
    <visual name="visual">
      <pose>0 -3 0 0 0 0</pose>
      <geometry>
        <cylinder>
          <radius>0.3</radius>
          <length>0.1</length>
        </cylinder>
      </geometry>
      <material><script><name>Gazebo/Red</name></script></material>
    </visual>
  </link>
</model>

</world>
</sdf>
