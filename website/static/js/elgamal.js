
async function postData(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(data),
    });
    return response.json();
}
document.addEventListener("DOMContentLoaded", function () {
    const generatePrimeBtn = document.querySelector(".generate-prime.btn");
    const submitBtn = document.querySelector(".generate-public-keys.btn");
    const encryptBtn = document.querySelector(".encrypt.btn");
    const decryptBtn = document.querySelector(".decrypt.btn");
    const generateAlphaBtn = document.querySelector(".generate-alpha.btn");
    const convertBtn = document.querySelector(".convert.btn");
    if(generatePrimeBtn){
        generatePrimeBtn.addEventListener("click", async () => {
    const bits = document.getElementById("bits").value;

    if (!bits || bits < 1 || bits > 1024) {
        alert("Bits must be between 1 and 1024.");
        return;
    }
    const data = await postData("/elgamal/genprime", { bits });
    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById("p").value =data.p;
    }
});
    }
    if(submitBtn){
        submitBtn.addEventListener("click", async () => {
    const p = document.getElementById("p").value;
    const alpha = document.getElementById("alpha").value;
    const a = document.getElementById("a").value;
    
    if (!p || !alpha || !a) {
        alert("Please enter values for p, alpha, a");
        return;
    }
    const data = await postData("/elgamal/genkey", { p, alpha, a });
    if (data.error) {
        alert(data.error);
    } else {
    document.getElementById("beta-value").innerText = `Result: β = ${data.beta}`;
    document.getElementById("public-key").innerText = `Public Key: (p, alpha, β) = (${p}, ${alpha}, ${data.beta})`;
    document.getElementById("private-key").innerText = `Private Key: (a) = (${a})`;
    }
});
    }
if(encryptBtn){
    encryptBtn.addEventListener("click", async () => {
        const k = document.getElementById("k").value;
        const m = document.getElementById("m").value;
        const alpha = document.getElementById("alpha").value;
        const beta = document.getElementById("beta-value").innerText.split("= ")[1];
        const p = document.getElementById("p").value;
       
        if (!k || !m || !alpha || !beta || !p) {
            alert("Please enter values for k, m, p, alpha, and beta.");
            return;
        }
        const data = await postData("/elgamal/encrypt", { k, m, alpha, beta,p });
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById("c1-value").innerText = `c1 = ${data.c1}`;
            document.getElementById("c2-value").innerText = `c2 = ${data.c2}`;
        }
        });
}
if(decryptBtn){
decryptBtn.addEventListener("click", async () => {
    const c1 = document.getElementById("c1-decrypt").value;
    const c2 = document.getElementById("c2-decrypt").value;
    const p = document.getElementById("p").value;
    const a = document.getElementById("a").value;

    if (!c1 || !c2 || !p || !a) {
        alert("Please enter values for c1, c2, p, and a.");
        return;
    }
    const data = await postData("/elgamal/decrypt", { c1, c2, p, a });
    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById("m-decrypt-value").innerText = `m = ${data.m}`;
    }
});
}
if(convertBtn){
    convertBtn.addEventListener("click", async () => {
    const plain = document.getElementById("plain").value;

    if (!plain) {
        alert("Please type your plaintext.");
        return;
    }

    const data = await postData("/elgamal", { plain });
    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById("plaintext").innerText = `Plaintext: ${data.plain}`;
    }
});
}
if(generateAlphaBtn){
    generateAlphaBtn.addEventListener("click", async () => {
    const p = document.getElementById("p").value;

    if (!p) {
        alert("Please enter p value for a.");
        return;
    }

    const data = await postData("/elgamal/genalpha", { p });
    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById("alpha").value = data.alpha;
    }
});
}
});