#!/bin/bash

# Executes a simple post request to the deployed model container.

curl -i -d '{
"instances": [
	{"input": [[[0.7467306 ],
        [0.90236002],
        [0.36139896],
        [0.63846154],
        [0.0734545 ],
        [0.12593601],
        [0.16363636]],

       [[0.74629468],
        [0.90236002],
        [0.3626943 ],
        [0.63846154],
        [0.06494875],
        [0.12593601],
        [0.16363636]],

       [[0.74760244],
        [0.90421101],
        [0.35880829],
        [0.64615385],
        [0.06380102],
        [0.12389381],
        [0.16090909]],

       [[0.77244987],
        [0.90421101],
        [0.33419689],
        [0.66923077],
        [0.07494812],
        [0.172226  ],
        [0.20909091]],

       [[0.76373147],
        [0.90421101],
        [0.31217617],
        [0.69230769],
        [0.05721338],
        [0.18243703],
        [0.22363636]],

       [[0.78378378],
        [0.90421101],
        [0.29404145],
        [0.70769231],
        [0.06024778],
        [0.21919673],
        [0.25909091]],

       [[0.78291194],
        [0.90282277],
        [0.27849741],
        [0.72307692],
        [0.0556726 ],
        [0.22736555],
        [0.26818182]],

       [[0.79250218],
        [0.90282277],
        [0.26683938],
        [0.73076923],
        [0.0532042 ],
        [0.26208305],
        [0.30363636]],

       [[0.78465562],
        [0.90328552],
        [0.28108808],
        [0.72307692],
        [0.0591315 ],
        [0.24846835],
        [0.29090909]]]
	}

	]
}' -X POST http://localhost:80/v1/models/cnn_model:predict --output -
