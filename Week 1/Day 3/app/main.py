from .simple_task import create_task
import sys
from .task_service import validate_priority,validate_title,ValidationError
def run_cli():
    print("running cli")
    raw_user_input={}
    try:
        #taking data from user
        raw_user_input["title"]=input("Enter title here:")
        raw_user_input["priority"]=input("Enter priority:")
    except ValueError:
        print("Transport Error: Enter valid priority")
        sys.exit()
    print("Now calculating")
    try:
        mock_next_id=1
        result=create_task(raw_user_input,mock_next_id)
        assert "id" not  in result,"Mutated input"
        print("Success:Task created successfully")
        print(result)
    except ValidationError as err:
        print("Validation Rule broken")
        print (err)
        sys.exit(1)
if __name__=="__main__":
    run_cli()