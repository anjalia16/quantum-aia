namespace NEQR {

    open Microsoft.Quantum.Core;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;

    // Encodes NEQR into the given registers from a classical image
    operation EncodeNEQR(color_register: Qubit[], y_register: Qubit[], x_register: Qubit[], image: Int[][]) : Unit {
        // Check lengths
        EqualityFactI(
            Length(color_register), 
            8, 
            "Color register was length " + IntAsString(Length(color_register)) + ", should be 8"
        );
        EqualityFactI(
            Length(y_register), 
            Ceiling(Lg(IntAsDouble(Length(image) + 1))), 
            "Y position register was length " + IntAsString(Length(y_register)) + ", should be " + IntAsString(Ceiling(Lg(IntAsDouble(Length(image) + 1))))
        );
        EqualityFactI(
            Length(x_register), 
            Ceiling(Lg(IntAsDouble(Length(image[0]) + 1))),
            "X position register was length " + IntAsString(Length(x_register)) + ", should be " + IntAsString(Ceiling(Lg(IntAsDouble(Length(image[0]) + 1))))
        );

        ApplyToEach(H, y_register);
        ApplyToEach(H, x_register);

        for y in 0 .. Length(image) - 1 {
            for x in 0 .. Length(image[0]) - 1 {

                let color_le = IntAsBoolArray(image[y][x], Length(color_register));

                SetPositionControls(y_register, x_register, y, x);

                for i in 0 .. Length(color_le) - 1 {
                    if color_le[i] {
                        Controlled X(y_register + x_register, color_register[i]);
                    }
                }

                Adjoint SetPositionControls(y_register, x_register, y, x);

            }
        }
    }

    // Produces a measurement from an image encoded into NEQR
    operation EncodeNEQRResult(image: Int[][]) : Result[] {
        use color_register = Qubit[8];
        use y_register = Qubit[Ceiling(Lg(IntAsDouble(Length(image) + 1)))];
        use x_register = Qubit[Ceiling(Lg(IntAsDouble(Length(image[0]) + 1)))];

        EncodeNEQR(color_register, y_register, x_register, image);
        let result = MultiM(color_register + y_register + x_register);
        ResetAll(color_register + y_register + x_register);
        return result;
    }

    // Set all qubits at 0 to 1 to allow for only this position to control the colors
    operation SetPositionControls(y_controls : Qubit[], x_controls : Qubit[], y_pos : Int, x_pos : Int) : Unit is Adj {
        let y_le = IntAsBoolArray(y_pos, Length(y_controls));
        let x_le = IntAsBoolArray(x_pos, Length(x_controls));

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