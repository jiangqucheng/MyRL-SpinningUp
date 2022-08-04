from datetime import datetime

TIME_STR_STYLE = "%H%M%S"

def get_time_str():
    return datetime.now().strftime(TIME_STR_STYLE)

file_handle = open(f"/workspace/Event_{get_time_str()}.txt", "w+")

try:
	import mujoco_py
	pass
except Exception as e:
	print( e )
	print( f"{get_time_str()}: fail", file=file_handle )
	print( e, file=file_handle )
	raise
else:
	print( f"{get_time_str()}: success" )
	print( f"{get_time_str()}: success.\n", file=file_handle )
	pass
finally:
	print( f"{get_time_str()}: done" )
	print( f"{get_time_str()}: done.\n", file=file_handle )
	pass
