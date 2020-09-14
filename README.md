# What this utility does:
- This utility modifies the internal renpy loader to allow it to read files at absolute paths on UNIX based systems
- It also removes the need for `config.reject_backslash`, opting to always replace them with forward slashes instead
  - This allows local paths made using backslashes, for example `mod_assets\bgm\song.ogg`, automatically be converted to `mod_assets/bgm/song.ogg`

# Why is this even a problem?
- This is a problem because it means accessing files in the `basedir` (Base directory, or in other words, the folder where you'd run the DDLC executable) is impossible without a full path. Additionally, in your own submodding ventures, personal or not, you may want to load files from outside the game's directory. The flaw in the loader would make this impossible.

# What causes this issue?
- This is effectively caused by Ren'Py's loader calling the `lstrip` function on the filepath it's told to load
- This function accepts an argument, and will remove all occurrences of that argument from the leftmost side of the string

# So how does this affect filepaths?
- Simply put, the `lstrip` function is given a `"/"` argument. Meaning it will remove all `/` characters from the start of the filepath
  - All UNIX paths ***start*** with `/`, and as such, their paths break. For example, `/home/user/Desktop/...` turns into `home/user/Desktop/...`. Which isn't valid.

- Windows gets away with this because of its *drive letters*. Since `C:/Users/User/Desktop/...` doesn't start with `/`, it doesn't change, making the path valid.

This utility is compatible with the [Submod Updater Plugin](https://github.com/Booplicate/MAS-Submods-SubmodUpdaterPlugin/releases/latest)! Give it an install to make updating this utility easier.

### Please report any and all problems in the `issues` tab.
###### Thank you
