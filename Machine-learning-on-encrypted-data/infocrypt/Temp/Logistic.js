function train(epochs, alpha){
    let errors =[];
    let A = 0.0;
    let B = 0.0;
    let C = 0.0;
    var count =0;
    var data = generateData(20,10,100,20);
    console.log(data.length);
    for (var i=0; i<epochs; i++){
        var error;
        console.log(data.length);
        data.forEach(d => {
            var predY;
            var func;
            func = A*d.x1/100+B*d.x2/100+C;
            predY = 1/(1+Math.exp(-func));
            error = predY - d.y;
            let tempA = A;
            let tempB = B;
            let tempC = C;

            A = tempA + alpha*-error*predY*(1-predY)*d.x1/100;
            B = tempB + alpha*-error*predY*(1-predY)*d.x2/100;
            C = tempC + alpha*-error*predY*(1-predY)*1.0;
        });

        console.log('A', A, 'B', B, 'C', C);
        console.log('Error', error);
        errors.push({error:error, epoch:i});

        var accuracy = 1+Math.round(error*100)/100;
        console.log(accuracy)
        console.log(errors);
    }

    

}

train(10,0.2);