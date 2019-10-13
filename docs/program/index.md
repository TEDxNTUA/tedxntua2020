# Program application
Responsible for the Speakers and the Schedule pages. Defines the `Activity` and `Presenter` models with a many-to-many relationship between them in order to provide a generic implementation.

## Models

### Presenter
Attributes:
* `first`: First name.
* `last`: Last name.
* `occupation`: Occupation (optional, mainly used for speakers).
* `short_bio`: Short bio (optional, mainly used for speakers).
* `quote`: Inspirational quote (optional, mainly used for speakers).
* `link`: URL to a personal website or social media profile (optional, mainly used for speakers).
* `image`: A picture of the Presenter.

Computed attributes:
* `fullname`: Full name (concatenation of `first` and `last`).

Managers:
* `speakers`: Gets all presenters that have at least one Activity of Talk type linked to them (e.g. `Presenter.speakers.all()`).
* `performers`: The same for presenters with at least one Performance Activity.
* `workshop_presenters`: The same for presenters with at least one Workshop Activity.

### Activity
Attributes:
* `activity_type`: One of {`T` = Talk, `P` = Performance, `W` = Workshop, `H` = Hosting}.
* `start`: Start time.
* `end`: End time.
* `title`: Title.
* `subtitle`: Summary with length of 1-2 sentences.
* `description`: Full description.
* `image`: A picture of the Activity (optional).

Managers:
* `talks`: Can be used to get all activities of Talk type (e.g. `Activity.talks.all()`).
* `performances`: The same for activities of Performance type.
* `workshops`: The same for activities of Workshop type.
