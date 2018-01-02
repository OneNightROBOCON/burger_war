<?xml version="1.0" ?>
<sdf version="1.4">
<world name="onigiri_field">
<gui>
  <camera name="camera">
    <pose>3 -2 3.5 0.0 .85 2.4</pose>
    <view_controller>orbit</view_controller>
  </camera>
</gui>
<include><uri>model://sun</uri></include>
<include><uri>model://ground_plane</uri></include>
@{box_count = 0}
@{tag_count = 0}
<!-- Centor BOX -->
<include>
  <name>box_@(box_count)</name>
  <pose>0 0 0.2 0 0 0</pose>
  <uri>model://center_box</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>0 -0.25 0.15 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.12 0.01 0.12</size></box></geometry>
      <material>
        <script>
          <uri>model://corner_box/tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>0 0.25 0.15 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.12 0.01 0.12</size></box></geometry>
      <material>
        <script>
          <uri>model://corner_box/tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>-0.25 0 0.15 0 0 1.571</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.12 0.01 0.12</size></box></geometry>
      <material>
        <script>
          <uri>model://corner_box/tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>0.25 0 0.15 0 0 1.571</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.12 0.01 0.12</size></box></geometry>
      <material>
        <script>
          <uri>model://corner_box/tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
@{box_count += 1}

<!-- Corner BOX -->
@{side_pos = 0.74}
@[for x in [-side_pos, side_pos]]
@[for y in [-side_pos, side_pos]]
<include>
  <name>box_@(box_count)</name>
  <pose>@(x) @(y) 0.2 0 0 0</pose>
  <uri>model://corner_box</uri>
</include>
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>@(x) @(y-0.1) 0.15 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.12 0.01 0.12</size></box></geometry>
      <material>
        <script>
          <uri>model://corner_box/tags</uri>
          <name>@(str(tag_count).zfill(4))</name>
        </script>
      </material>
    </visual>
  </link>
</model>
@{tag_count += 1}
<model name="box_@(box_count)_tag_@(tag_count)">
  <static>true</static>
  <pose>@(x) @(y+0.1) 0.15 0 0 0</pose>
  <link name="link">
    <visual name="visual">
      <geometry><box><size>0.12 0.01 0.12</size></box></geometry>
      <material>
        <script>
          <uri>model://corner_box/tags</uri>
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
  @{thickness_y = 0.05}
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
      </visual>
    </link>
  </model>
@[end def]
@{wall.count = 0}
@{wall_size = 2.475}
@( wall((0, wall_size), (wall_size, 0), 0.5) )
@( wall((wall_size, 0), (0, -wall_size), 0.5) )
@( wall((0, -wall_size), (-wall_size, 0), 0.5) )
@( wall((-wall_size, 0), ( 0, wall_size), 0.5) )
</world>
</sdf>
