const crypto = require('crypto-js');
function _stringify(e) {
                            for (var t = e.words, n = e.sigBytes, r = [], i = 0; i < n; i++) {
                                var o = t[i >>> 2] >>> 24 - i % 4 * 8 & 255;
                                r.push((o >>> 4).toString(16)),
                                r.push((15 & o).toString(16))
                            }
                            return r.join("")
                        }

function get_sha3_encrypt(data,outputLengthNum) {
    const hash = crypto.SHA3(data, { outputLength: outputLengthNum })
    const r = {
                words: hash.words,
                sigBytes: hash.sigBytes
            };
    return _stringify(r)
}

