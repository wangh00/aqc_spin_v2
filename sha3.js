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
function fillZero(t=1) {
                let e = "";
                for (var r = 0; r < t; r++)
                    e += "0";
                return e
            }


function pow(data) {
    var e = JSON.parse(data);
    let encrypts={'sha1Pow':crypto.SHA1,'md5Pow':crypto.MD5};
    const r = fillZero(e.count)
      , i = Date.now();
    let n, o = 0, s = "0";
    for (; s !== r; )
        s = _stringify(encrypts[e.version](e.originStr['spin-0'] + o)).substring(0, e.count),
        o++;
    return n = Date.now() - i,
    {
        t: n,
        an: o - 1
    }
}


console.log(pow(JSON.stringify({count:3,list:['spin-0'],originStr:{'spin-0':"7214b764c4c63ef07684dd58029781e177832ed0"},version:"sha1Pow"})))
//
// console.log(_stringify(crypto.SHA1('07c4865fb25d53cc9e61d032dbe5fec45958bab10')))