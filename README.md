# Auto Story Poster

A Python-based automation tool that generates Instagram story images with captions and posts them. The project consists of two scripts:

1. `add-story.py`: Creates images with captions.
2. `post-story.py`: Posts the generated images to Instagram using `instagrapi`.

---

## Features

- Automatically generates Instagram story images with captions.
- Customizable background and font for the stories.
- Posts stories directly to Instagram for either "Close Friends" or public audiences.
- Archives posted stories to a separate folder.
- Tracks last posting time to ensure stories are posted daily.

---


## Usage

### Script 1: `add-story.py`

This script generates story images with the provided captions.

#### Command:

```bash
python add-story.py <caption_story_1> <caption_story_2> ...
```

#### Example:

```bash
python add-story.py "Caption for first story" "Caption for second story"
```

#### Outputs:

- Story images are saved in the `queue` folder, named with a timestamp.

---

### Script 2: `post-story.py`

This script posts the generated story images to Instagram. It uses the credentials stored in environment variables.
- Set up environment variables for Instagram credentials:

```bash
export USER="your_instagram_username"
export PASS="your_instagram_password"
```

#### Command:

```bash
python post-story.py [-nc | --no-close]
```

#### Arguments:

- `-nc`, `--no-close`: Post the stories publicly instead of for "Close Friends."

#### Example:

- Post for "Close Friends":

  ```bash
  python post-story.py
  ```

- Post publicly:

  ```bash
  python post-story.py --no-close
  ```

---

