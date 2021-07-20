namespace NEQR {

    open Microsoft.Quantum.Core;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;

    operation EncodeNEQR(image: Int[][]) : Qubit[] {
        use color_register = Qubit[8];
        use y_register = Qubit[Ceiling(Lg(Length(image)))];
        use x_register = Qubit[Ceiling(Lg(Length(image[0])))];

        ApplyToEach(H, position_y);
        ApplyToEach(H, position_x);

        for y in 0 .. Length(image) {
            for x in 0 .. Length(image[0]) {

                let color_le = IntAsBoolArray(image[y][x]);

                SetPositionControls(y_register, x_register, y, x);

                for i in 0 .. Length(color_le) - 1 {
                    if color_le[i] {
                        Controlled X(y_register + x_register, colors[i]);
                    }
                }

                Adjoint SetPositionControls(y_register, x_register, y, x);

            }
        }

        return color_register + y_register + x_register;
    }

    operation EncodeNEQRResult(image: Int[][]) : Result[] {
        return MultiM(EncodeNEQR(image));
    }

    // Set all qubits at 0 to 1 to allow for only this position to control the colors
    operation SetPositionControls(y_controls : Qubit[], x_controls : Qubit[], y_pos : Int, x_pos : Int) : Unit is Adj {
        let y_le = IntAsBoolArray(y_pos);
        let x_le = IntAsBoolArray(x_pos);

        for i in 0 .. Length(y_le) - 1 {
            if not y_le[i] {
                X(y_controls[i]);
            }
        }

        for i in 0 .. Length(x_le) - 1 {
            if not x_le[i] {
                X(x_controls[i]);
            }
        }
    }

    
}