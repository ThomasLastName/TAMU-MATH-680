
# ~~~ Tom Winckelman wrote this; maintained at: https://github.com/ThomasLastName/labs_680

exercise_mode = False   # ~~~ see https://github.com/ThomasLastName/labs_680?tab=readme-ov-file#usage
install_assist = False  # ~~~ see https://github.com/ThomasLastName/labs_680?tab=readme-ov-file#assisted-installation-for-environments-other-than-colab-deprecated


### ~~~
## ~~~ Boiler plate stuff; basically just loading packages
### ~~~

#
# ~~~ Standard python libraries
import torchvision
import torch
from torch import nn

#
# ~~~ see https://github.com/ThomasLastName/labs_680?tab=readme-ov-file#assisted-installation-for-environments-other-than-colab-deprecated
import os
this_is_running_in_colab = os.getenv("COLAB_RELEASE_TAG")   # ~~~ see https://stackoverflow.com/a/74930276
if install_assist or this_is_running_in_colab:              # ~~~ override necessary permissions if this is running in Colab
    confirm_permission_to_modify_files = not install_assist
    if (install_assist and confirm_permission_to_modify_files) or this_is_running_in_colab:
        #
        # ~~~ Base package for downloading files
        from urllib.request import urlretrieve
        #
        # ~~~ Define a routine that downloads a raw file from GitHub and locates it at a specified path
        def download_dotpy_from_GitHub_raw( url_to_raw, file_name, folder_name, deisred_parent_directory=None, verbose=True ):
            #
            # ~~~ Put together the appropriate path
            this_is_running_in_colab = os.getenv("COLAB_RELEASE_TAG")   # ~~~ see https://stackoverflow.com/a/74930276
            parent_directory = os.path.dirname(os.path.dirname(torch.__file__)) if (deisred_parent_directory is None) else deisred_parent_directory
            parent_directory = "" if this_is_running_in_colab else parent_directory
            folder_path = os.path.join( parent_directory, folder_name )
            file_path = os.path.join( folder_path, file_name )
            print_path = os.path.join("/content",folder_name,file_name) if this_is_running_in_colab else file_path
            #
            # ~~~ Create the folder if it doesn't already exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                if verbose:
                    print("")
                    print(f"Folder {folder_name} created at {os.path.dirname(print_path)}")
                    print("")
            #
            # ~~~ Download that file and place it at the path `file_path`, overwritting a file of the same name in the same location, if one exists
            prefix = "Updated" if os.path.exists(file_path) else "Created"
            urlretrieve( url_to_raw, file_path )
            if verbose:
                suffix = " (click the folder on the left)" if this_is_running_in_colab else ""
                print( f"{prefix} file {file_name} at {print_path}{suffix}" )
        #
        # ~~~ A routine that downloads from Tom's GitHub repos
        def intstall_Toms_code( folder_name, files, repo_name=None, verbose=True ):
            repo_name = folder_name if repo_name is None else repo_name
            base_url = f"https://raw.githubusercontent.com/ThomasLastName/{repo_name}/main/"
            for file_name in files:
                download_dotpy_from_GitHub_raw( url_to_raw=base_url+file_name, file_name=file_name, folder_name=folder_name, verbose=verbose )
        #
        # ~~~ "Install/update" quality_of_life
        folder = "quality_of_life"
        files = [ "ansi.py", "my_base_utils.py", "my_torch_utils.py" ]
        intstall_Toms_code( folder, files )
        #
        # ~~~ "Install/update" answers_680
        folder = "answers_680"
        files = [ "answers_week_10.py" ]
        intstall_Toms_code( folder, files )

#
# ~~~ Tom's helper routines (which the above block of code installs for you); maintained at https://github.com/ThomasLastName/quality_of_life
from quality_of_life.my_torch_utils import convert_Dataset_to_Tensors, convert_Tensors_to_Dataset
from quality_of_life.my_base_utils import support_for_progress_bars



### ~~~
## ~~~ EXERCISE 1 of 5: Download MNIST
###  ~~~

#
# ~~~ Set the parent directory where you want to store data on your computer
my_data_directory = "C:\\Users\\thoma\\AppData\\Local\\Programs\\Python\\Python310\\pytorch_data"

MNIST_train = torchvision.datasets.MNIST(
        root = my_data_directory,   # where to look for the data on your computer (if the data isn't there and download=True, then it will download the data and put it there)
        train = True,               # specify whether you want the training data or the test data
        download = True,            # give permission to download the data if pytorch doesn't find it in `root`
        transform = torchvision.transforms.ToTensor()   # convert whatever weird format .jpeg data comes into an actual mathematical object
    )

MNIST_test = torchvision.datasets.MNIST(
        root = my_data_directory,   # where to look for the data on your computer (if the data isn't there and download=True, then it will download the data and put it there)
        train = False,              # specify whether you want the training data or the test data
        download = True,            # give permission to download the data if pytorch doesn't find it in `root`
        transform = torchvision.transforms.ToTensor()   # convert whatever weird format .jpeg data comes into an actual mathematical object
    )



### ~~~
## ~~~ EXERCISE 2 of 5: Get the actual data out of pytorch's Dataset class
### ~~~

if exercise_mode:
    #
    # ~~~ write a function that excracts the actual matrices from `MNIST_train` and `MNIST_test`
    def get_data(object_of_class_Dataset):
        # HINT objects of class torch.utils.data.Dataset aren't matrices but you can still " do [index] to them;" try printing `MNIST_train[0]` (this works thanks to the __getitem__ method; see https://pytorch.org/tutorials/beginner/basics/data_tutorial.html#getitem)
        return X, y
else:
    from quality_of_life.my_torch_utils import convert_Dataset_to_Tensors as get_data


X_test, y_test = convert_Dataset_to_Tensors(MNIST_test)         # ~~~ correct implementation
my_X_test, my_y_test = get_data(MNIST_test)                     # ~~~ my implementation
assert (X_test==my_X_test).min() and (y_test==my_y_test).min()  # ~~~ check that the results are identical




### ~~~
## ~~~ EXERCISE 3 of 5: Build a torch.utils.data.Dataset out of plain old numbers
### ~~~

if exercise_mode:
    #
    # ~~~ write a function that assembles actual matrices into objects of class torch.utils.data.Dataset like `MNIST_train` and `MNIST_test`
    def assemble_data(object_of_class_Dataset):
        # HINT this is highly googlable
        return Dataset
else:
    #
    # ~~~ load my left inverse to get_data; note that my implelemntation is *not* a bijection: we have get(assemble(v))=v, but *not* assemble(get(w))=w
    from quality_of_life.my_torch_utils import convert_Tensors_to_Dataset as assemble_data



my_X, my_y = get_data(assemble_data(X_test,y_test))     # ~~~ build a torch.utils.data.Dataset and then call the tensors that we built it out of
assert (X_test==my_X).min() and (y_test==my_y).min()    # ~~~ check that we got back exactly what we started with



### ~~~
## ~~~ EXERCISE 4 of 5: Identify where a,b,c,d,e,f,g,h below are valid, and which of them are identical to which others
### ~~~

if exercise_mode:
    #
    # ~~~ Delete any of these that are invalid; determine which are identical to which others
    a = torch.Tensor([3,1,0])
    b = torch.tensor([3,1,0])
    c = torch.Tensor([3.,1.,0.])
    d = torch.tensor([3.,1.,0.])
    e = torch.Tensor([3.,1.,0.], dtype=torch.int32)
    f = torch.tensor([3.,1.,0.], dtype=torch.int32)
    g = torch.Tensor([3.,1.,0.], dtype=torch.int64)
    h = torch.tensor([3.,1.,0.], dtype=torch.int64)



### ~~~
## ~~~ EXERCISE 5 of 5 (medium): Reproduce a pytorch dataloader
### ~~~

if exercise_mode:
    #
    # ~~~ Write a function that takes a pytorch dataset as input, and splits the data and label into batches of the desired size, optionally shuffling those batches
    def my_dataloader( Dataset, batch_size=1, shuffle=False ):
        all_X, all_y = convert_Dataset_to_Tensors(Dataset)
        # YOUR CODE HERE which rearranges the data if `shuffle==True`
        X_batches = a_list_of_tensors       # YOUR CODE HERE which splilts the data into subsets of size `batch_size`
        y_batches = another_list_of_tensors # YOUR CODE HERE which splilts the data into subsets of size `batch_size`
        return tuple(zip(X_batches,y_batches))
else:
    from answers_680.answers_week_10 import my_dataloader

#
# ~~~ Validate your implementation
unofficial_dataloader = my_dataloader( MNIST_train, batch_size=40 )
official_dataloader = torch.utils.data.DataLoader( MNIST_train, batch_size=40 )
try:
    for j,(X,y) in enumerate(official_dataloader):
        (XX,yy) = unofficial_dataloader[j]
        assert (X==XX).all() and (y==yy).all()
    print("Success!")
except AssertionError:
    print("Failure! Try Again!")




