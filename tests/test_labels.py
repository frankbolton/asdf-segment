from asdf_segment.labels import LabelModel, NUM_LABELS


def test_default_labels():
    model = LabelModel()
    assert len(model.labels) == NUM_LABELS
    assert model.active_row == 0
    assert model.active_label.index == 1


def test_step_active_clamps_and_wraps_within_bounds():
    model = LabelModel()
    model.step_active(-1)
    assert model.active_row == 0  # clamped, not wrapped

    model.set_active_row(NUM_LABELS - 1)
    model.step_active(1)
    assert model.active_row == NUM_LABELS - 1  # clamped at top


def test_active_changed_signal_fires_on_change_only():
    model = LabelModel()
    seen = []
    model.active_changed.connect(seen.append)

    model.set_active_row(0)  # no-op, same row
    assert seen == []

    model.set_active_row(3)
    assert seen == [3]


def test_color_map_includes_transparent_default():
    model = LabelModel()
    color_map = model.color_map()
    assert color_map[None] == "#00000000"
    assert color_map[1] == model.labels[0].color
