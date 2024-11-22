document.addEventListener("DOMContentLoaded", function () {
    const generatePrimeBtn = document.querySelector(".generate-prime.btn");
    const generatepointBtn = document.querySelector(".generate-point.btn");
    if(generatePrimeBtn){
        generatePrimeBtn.addEventListener("click", async () => {
        const bits = document.getElementById("bits").value;
    
        if (!bits) {
            alert("Please enter the number of bits to generate a prime number .");
            return;
        }
    
        const data = await postData("/elliptic_signature/genprime", { bits });
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