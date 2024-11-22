async function postData(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(data),
    });
    return response.json();
}
function findPointByCoordinates(x, y, points) {
    const point = points.find((point) => point.x === x && point.y === y);
    return point ? point : null;
}
function convertStringToArray(str) {
    str = str.replace(/[()]/g, '');

    let arr = str.split(',');
    arr = arr.map(Number);

    return arr;
}

function modPower(base, exponent, modulus) {
    let result = 1;
    base = base % modulus;
    while (exponent > 0) {
        if (exponent % 2 === 1) { 
            result = (result * base) % modulus;
        }
        exponent = Math.floor(exponent / 2);
        base = (base * base) % modulus;
    }
    return result;
}

function str2int(m) {
    let p = 0;
    let b = 1;

    for (let i = m.length - 1; i >= 0; i--) {
        const p_i = ((m[i].toUpperCase().charCodeAt(0) - 65) % 26 + 26) % 26;
        p += p_i * b;
        b *= 26;
    }

    return p;
}
function elGamalEncrypt(p, a, P, m , k,B) {
    const C1 = scalarMultiplication(k, P, a, p);
    const tmp = scalarMultiplication(k, B, a, p);
    const C2 = pointAddition(m,tmp, a, p);
    return { C1, C2 };
}

function elGamalDecrypt(p, a, b, s, C1, C2) {
    const sC1 = scalarMultiplication(s, C1, a, p);
    const Q = [sC1[0], -sC1[1]];
    const M = pointAddition(C2, Q, a, p);
    return { x: M[0], y: M[1] };
}

function int2str(p) {
    let m = "";

    while (p > 0) {
        const r = p % 26; // Lấy phần dư
        m = String.fromCharCode(r + 65) + m; 
        p = Math.floor((p - r) / 26); 
    }

    return m;
}

function isValidCurve(a, b, p) {
    const discriminant = (4 * Math.pow(a, 3) + 27 * Math.pow(b, 2)) % p;
    return discriminant !== 0;
}

function createEllipticCurve(a, b, p) {
    if (!isValidCurve(a, b, p)) {
        throw new Error("Invalid curve: discriminant is zero.");
    }
    return { a, b, p };
}


function mod(n, p) {
    return ((n % p) + p) % p;
}
function isQuadraticResidue(n, p) {
    for (let y = 0; y < p; y++) {
        if (mod(y * y, p) === mod(n, p)) {
            return true;
        }
    }
    return false;
}


function findY(n, p) {
    const solutions = [];
    for (let y = 0; y < p; y++) {
        if (mod(y * y, p) === mod(n, p)) {
            solutions.push(y);
        }
    }
    return solutions;
}
function findPointsOnCurve(a, b, p) {
    const points = [];

    for (let x = 0; x < p; x++) {
        const rhs = mod(Math.pow(x, 3) + a * x + b, p); 

        if (isQuadraticResidue(rhs, p)) {
            const yValues = findY(rhs, p); 
            yValues.forEach((y) => points.push({ x, y }));
        }
    }

    return points;
}
function pointAddition(P, Q, a, p) {
    if (!P || !Q) return null;

    const [x1, y1] = P;
    const [x2, y2] = Q;

    if (x1 === x2 && y1 === -y2) return null; 

    let m;
    if (x1 === x2 && y1 === y2) {
        m = mod((3 * x1 ** 2 + a) * modInverse(2 * y1, p), p);
    } else {

        m = mod((y2 - y1) * modInverse(x2 - x1, p), p);
    }

    const x3 = mod(m ** 2 - x1 - x2, p);
    const y3 = mod(m * (x1 - x3) - y1, p);

    return [x3, y3];
}
function modInverse(a, p) {
    let m0 = p, t, q;
    let x0 = 0, x1 = 1;

    if (p === 1) return 0;

    while (a > 1) {
        q = Math.floor(a / p);
        t = p;
        p = a % p; a = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }

    if (x1 < 0) x1 += m0;

    return x1;
}

function scalarMultiplication(k, P, a, p) {
    let result = null;
    let addend = P;

    while (k > 0) {
        if (k % 2 === 1) {
            result = result ? pointAddition(result, addend, a, p) : addend;
        }
        addend = pointAddition(addend, addend, a, p); 
        k = Math.floor(k / 2);
    }

    return result;
}


document.addEventListener("DOMContentLoaded", function () {
const generatePrimeBtn = document.querySelector(".generate-prime.btn");
const generatepointBtn = document.querySelector(".generate-point.btn");
const encryptBtn = document.querySelector(".encrypt.btn");
const decryptBtn = document.querySelector(".decrypt.btn");
if(generatePrimeBtn){
    generatePrimeBtn.addEventListener("click", async () => {
    const bits = document.getElementById("bits").value;

    if (!bits) {
        alert("Please enter the number of bits to generate a prime number .");
        return;
    }

    const data = await postData("/elliptic/genprime", { bits });
    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById("p").value = data.p;
    }
});
}
        const generateEllipticBtn = document.querySelector(".generate-elliptic.btn");
        if (generateEllipticBtn) {
            generateEllipticBtn.addEventListener("click", () => {
                const p = parseInt(document.getElementById("p").value);
                const a = parseInt(document.getElementById("a").value);
                const b = parseInt(document.getElementById("b").value);
    
                if (!p || !a || !b) {
                    alert("Please enter values for p, a, and b.");
                    return;
                }
    
                try {
                    document.getElementById("curve").innerText = `y² = x³ + ${a}x + ${b} mod ${p}`;
                    const points = findPointsOnCurve(a, b, p);
                    const pointList = points.slice(0,30)
                        .map((point) => `(${point.x}, ${point.y})`)
                        .join(", ");
                    document.getElementById("points").innerText =
                        `Points on curve: ${pointList}`;
                } catch (e) {
                    alert(e.message);
                }
            });
        }
        if (!generatepointBtn) {
            console.error("Generate Point button not found!");
            return;
        }
    
        generatepointBtn.addEventListener("click", () => {
            const p = parseInt(document.getElementById("p").value);  
            const a = parseInt(document.getElementById("a").value);
            const b = parseInt(document.getElementById("b").value);
            const m = parseInt(document.getElementById("mm").value);
            const points = findPointsOnCurve(a, b, p);
            if (!p || !a || !b || !m) {
                alert("Please enter values for p, a, b, and m.");
                return;
            }
            const point = points.find((point) => point.x == m%p);
            document.getElementById("m").innerText = `(${point.x}, ${point.y})`;
        });
    
        const convertBtn = document.querySelector(".convert.btn");
        if (convertBtn) {
            convertBtn.addEventListener("click", () => {
                const plaintext = document.getElementById("plain").value.trim();
                if (!plaintext) {
                    alert("Please enter plaintext.");
                    return;
                }
                const plainAsNumber = str2int(plaintext);
                document.getElementById("mm").value = plainAsNumber;
            });
        }
        if (encryptBtn) {
        encryptBtn.addEventListener("click", () => {
            const p = parseInt(document.getElementById("p").value);
            const a = parseInt(document.getElementById("a").value);
            const P = [parseInt(document.getElementById("x").value), parseInt(document.getElementById("y").value)];
            const k = parseInt(document.getElementById("k").value);
            const m = document.getElementById("m").innerText; 
            const M = [parseInt(convertStringToArray(m)[0]),parseInt(convertStringToArray(m)[1])];
            const B = scalarMultiplication(s, P, a, p);
            console.log(B);
            if(!P || !M || !k || !s){
                alert("Please enter values for P, M, k, and s.");
                return;
            }
    const encrypted = elGamalEncrypt(p,a,P, M, k, B);
    document.getElementById("m1-value").innerText = `M1 = (${encrypted.C1})`;
    document.getElementById("m2-value").innerText = `M2 = (${encrypted.C2})`;
});
        }
if(decryptBtn){
decryptBtn.addEventListener("click", () => {
    const p = parseInt(document.getElementById("p").value);
    const a = parseInt(document.getElementById("a").value);
    const b = parseInt(document.getElementById("b").value);
    const s = parseInt(document.getElementById("s").value);
    const encrypted = {
        C1: [parseInt(document.getElementById("m1-decrypt").value), parseInt(document.getElementById("m2-decrypt").value)],
        C2: [parseInt(document.getElementById("m1-decrypt-y").value),parseInt(document.getElementById("m2-decrypt-y").value)]
    };
    const decrypted = elGamalDecrypt(p, a, b, s, encrypted.C1, encrypted.C2);
    document.getElementById("m-decrypt-value").innerText = `m = (${decrypted.x}, ${decrypted.y})`;
});
}

    const sInput = document.getElementById("s");
    const xInput = document.getElementById("x");
    const yInput = document.getElementById("y");
    const betaValue = document.getElementById("beta-value");
    const publicKeyDisplay = document.getElementById("public-key");
    const privateKeyDisplay = document.getElementById("private-key");

    function updateKeys() {
        const s = parseInt(sInput.value);
        const pX = parseInt(xInput.value);
        const pY = parseInt(yInput.value);
        const a = parseInt(document.getElementById("a").value);
        const b = parseInt(document.getElementById("b").value);
        const p = parseInt(document.getElementById("p").value);

        const P = [pX, pY];
        const B = scalarMultiplication(s, P, a, p);

        if (!B) {
            betaValue.innerText = "Invalid point or scalar.";
            publicKeyDisplay.innerText = "";
            privateKeyDisplay.innerText = "";
            return;
        }

        betaValue.innerText = `β = (${B[0]}, ${B[1]})`;
        publicKeyDisplay.innerText = `Public key: (p, a, b, P, B) = (${p}, ${a}, ${b}, (${P[0]}, ${P[1]}), (${B[0]}, ${B[1]}))`;
        privateKeyDisplay.innerText = `Private key: (s) = ${s}`;
    }

    sInput.addEventListener("input", updateKeys);
    xInput.addEventListener("input", updateKeys);
    yInput.addEventListener("input", updateKeys);
});