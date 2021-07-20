namespace NEQR {

    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;

    operation TestRandom() : Int {
        use q = Qubit();
        mutable result = new Result[0];
        for i in 0 .. 7 {
            set result += [M(q)];
            Reset(q);
        }
        return ResultArrayAsInt(result);
    }
}